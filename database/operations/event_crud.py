from database.models.event import (
    Events,Clients,Payments,EventsCompletedStatus,EventsPendingCanceledStatus,EventNames,EventStatusImages,NeivethiyamNames,EventsNeivethiyam,EventsContactDescription,EventsAssignments
)
from database.models.workers import Workers,WorkersParticipationLogs
from fastapi import BackgroundTasks,Request,File,UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select,func,desc,or_,and_
from enums import backend_enums
from security.uuid_creation import create_unique_id
from datetime import date,time
from pydantic import EmailStr
from fastapi.exceptions import HTTPException
from database.operations.user_auth import UserVerification
from typing import Optional
from utils import indian_time,notification_image_url
from datetime import datetime,timezone,timedelta
from icecream import ic
from firebase_db.operations import FirebaseCrud
from utils.push_notification import PushNotificationCrud
from utils.error_notification import send_error_notification
from database.operations.notification import NotificationsCrud

class __AddEventInputs:
    def __init__(
            self,
            bg_task:BackgroundTasks,
            session:Session,
            user_id:str,
            event_name:str,
            event_description:str,
            event_date:date,
            event_start_at:str,
            event_end_at:str,
            client_name:str,
            client_mobile_number:str,
            client_city:str,
            total_amount:int,
            paid_amount:int,
            payment_status:backend_enums.PaymetStatus,
            payment_mode:backend_enums.PaymentMode,
            neivethiyam_id:Optional[int]=None,
            is_special:Optional[bool]=None,
            padi_kg:Optional[int]=None
    ):
        self.user_id=user_id
        self.session=session
        self.event_name=event_name
        self.event_description=event_description
        self.event_date=event_date
        self.event_start_at=event_start_at
        self.event_end_at=event_end_at
        self.client_name=client_name
        self.client_mobile_number=client_mobile_number
        self.client_city=client_city
        self.total_amount=total_amount
        self.paid_amount=paid_amount
        self.payment_status=payment_status
        self.payment_mode=payment_mode
        self.neivethiyam_id=neivethiyam_id
        self.is_special=is_special
        self.padi_kg=padi_kg
        self.bg_task=bg_task

class __EventAndNeivethiyamNameAndAmountCrudInputs:
    def __init__(self,session:Session,user_id:str):
        self.session=session
        self.user_id=user_id

class __DeleteEventInputs:
    def __init__(self,session:Session,user_id:str):
        self.session=session
        self.user_id=user_id

class __UpdateEventCompletedStatusInputs:
    def __init__(
            self,
            session:Session,
            user_id:str,
            event_id:str,
            event_status:backend_enums.EventStatus,
            feedback:str,
            archagar:int,
            abisegam:int,
            helper:int,
            poo:int,
            read:int,
            prepare:int,
            image:Optional[bytes],
            image_url_path:str,
            bg_task:BackgroundTasks,
            request:Request
        ):
        self.session=session
        self.user_id=user_id
        self.event_id=event_id
        self.event_status=event_status
        self.feedback=feedback
        self.archagar=archagar
        self.abisegam=abisegam
        self.helper=helper
        self.poo=poo
        self.read=read
        self.prepare=prepare
        self.image=image
        self.image_url_path=image_url_path
        self.bg_task=bg_task
        self.request=request

class __UpdateEventPendingCanceledInputs:
    def __init__(
        self,
        session:Session,
        user_id:str,
        event_id:str,
        event_status:backend_enums.EventStatus,
        description:str,
        bg_task:BackgroundTasks
    ):
        self.session=session
        self.user_id=user_id
        self.event_id=event_id
        self.event_status=event_status
        self.description=description
        self.bg_task=bg_task

class __ContactDescriptionInputs:
    def __init__(self,session:Session,user_id:str):
        self.session=session
        self.user_id=user_id

class EventVerification:
    def __init__(self,session:Session):
        self.session=session

    async def is_event_exists_by_id(self,event_id:str):
        event=self.session.execute(select(Events).where(Events.id==event_id)).scalar_one_or_none()
        if event:
            return event
        raise HTTPException(
            status_code=404,
            detail="event not found"
        )
    
class NeivethiyamNameVerification:
    def __init__(self,session:Session):
        self.session=session
    
    async def is_neivethiyam_exists_by_id(self,neivethiyam_id):
        neivethiyam=self.session.execute(select(NeivethiyamNames.id).where(NeivethiyamNames.id==neivethiyam_id)).scalar_one_or_none()
        if neivethiyam:
            return neivethiyam
        raise HTTPException(
            status_code=404,
            detail="neivethiyam id not found"
        )
    
    async def is_neivethiyam_exists_by_id(self,neivethiyam_name):
        neivethiyam=self.session.execute(select(NeivethiyamNames.id).where(NeivethiyamNames.name==neivethiyam_name)).scalar_one_or_none()
        if neivethiyam:
            return neivethiyam
        raise HTTPException(
            status_code=404,
            detail="neivethiyam id not found"
        )
    
class EventNameVerification:
    def __init__(self,session:Session):
        self.session=session
    
    async def is_event_name_exists_by_id(self,event_name_id):
        event_name=self.session.execute(select(EventNames.id).where(EventNames.id==event_name_id)).scalar_one_or_none()
        if event_name:
            return event_name
        raise HTTPException(
            status_code=404,
            detail="event name id not found"
        )
    
    async def is_event_name_exists_by_name(self,event_name):
        event_name=self.session.execute(select(EventNames.id).where(EventNames.name==event_name)).scalar_one_or_none()
        if event_name:
            return event_name
        raise HTTPException(
            status_code=404,
            detail="event name not found"
        )


class EventNameAndAmountCrud(__EventAndNeivethiyamNameAndAmountCrudInputs):
    async def add_event_name_and_amt(self,event_name:str,event_amount:int,is_special:bool):
        try:
            with self.session.begin():
                user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    is_event_name_exists=self.session.execute(select(EventNames.name).where(EventNames.name==event_name)).scalar_one_or_none()
                    if not is_event_name_exists:
                        added_event_name=EventNames(
                            name=event_name,
                            amount=event_amount,
                            is_special=is_special
                        )
                        self.session.add(added_event_name)
                        return "successfully event name added"
                    raise HTTPException(
                        status_code=409,
                        detail="Event name already exists"
                    )
                raise HTTPException(
                    status_code=401,
                    detail='you are not allowed to make any changes'
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="something went wrong while adding event name"
            )
        
    async def delete_event_name_and_amount(self,event_name):
        try:
            with self.session.begin():
                user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    en_to_delete=self.session.query(EventNames).filter(EventNames.name==event_name).first()
                    if en_to_delete:
                        self.session.delete(en_to_delete)
                    else:
                        raise HTTPException(
                            status_code=404,
                            detail="event name id not found"
                        )

                    return 'successfully event name deleted'
                raise HTTPException(
                    status_code=401,
                    detail='you are not allowed to make any changes'
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while adding event name {e}"
            )
    
    async def get_event_name_and_amount(self):
        try:
            user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)
            if user.role==backend_enums.UserRole.ADMIN:
                event_names=self.session.execute(
                    select(
                        EventNames.id,
                        EventNames.name,
                        EventNames.amount,
                        EventNames.is_special
                    )
                    .order_by(desc(EventNames.id))
                ).mappings().all()

                return {"event_names":event_names}
            raise HTTPException(
                status_code=401,
                detail='you are not allowed to get this information'
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while getting event name {e}"
            )
        
class NeivethiyamNameAndAmountCrud(__EventAndNeivethiyamNameAndAmountCrudInputs):
    async def add_neivethiyam_name_and_amt(self,neivethiyam_name:str,neivethiyam_amount:int):
        try:
            with self.session.begin():
                user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    is_neivethiyam_name_exists=self.session.execute(select(NeivethiyamNames.name).where(NeivethiyamNames.name==neivethiyam_name)).scalar_one_or_none()
                    if not is_neivethiyam_name_exists:
                        added_event_name=NeivethiyamNames(
                            name=neivethiyam_name,
                            amount=neivethiyam_amount
                        )
                        self.session.add(added_event_name)
                        return "successfully neivethiyam name added"
                    raise HTTPException(
                        status_code=409,
                        detail="Neivethiyam name already exists"
                    )
                raise HTTPException(
                    status_code=401,
                    detail='you are not allowed to make any changes'
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="something went wrong while adding neivethiyam name"
            )
        
    async def delete_neivethiyam_name_and_amount(self,neivethiyam_name):
        try:
            with self.session.begin():
                user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    nv_to_delete=self.session.query(NeivethiyamNames).filter(NeivethiyamNames.name==neivethiyam_name).first()
                    if nv_to_delete:
                        self.session.delete(nv_to_delete)
                    else:
                        raise HTTPException(
                            status_code=404,
                            detail="neivethiyam name not found"
                        )

                    return 'successfully neivethiyam name deleted'
                raise HTTPException(
                    status_code=401,
                    detail='you are not allowed to make any changes'
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while deleting neivethiyam name {e}"
            )
    
    async def get_neivethiyam_name_and_amount(self):
        try:
            user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)
            if user.role==backend_enums.UserRole.ADMIN:
                neivethiyam_names=self.session.execute(
                    select(
                        NeivethiyamNames.id,
                        NeivethiyamNames.name,
                        NeivethiyamNames.amount
                    )
                    .order_by(desc(NeivethiyamNames.id))
                ).mappings().all()

                return {"neivethiyam_names":neivethiyam_names}
            raise HTTPException(
                status_code=401,
                detail='you are not allowed to get this information'
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while getting neivethiyam name {e}"
            )
                    
class AddEvent(__AddEventInputs):
    async def add_event(self):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:

                    is_event_name_exists=self.session.execute(select(EventNames.id).where(EventNames.name==self.event_name)).scalar_one_or_none()
                    ic("hello",is_event_name_exists)
                    is_neivethiyam_name_exists=self.session.execute(select(NeivethiyamNames.id).where(NeivethiyamNames.id==self.neivethiyam_id)).scalar_one_or_none()
                    ic("hello",is_event_name_exists,is_neivethiyam_name_exists)
                    if not is_event_name_exists and not is_neivethiyam_name_exists:
                        raise HTTPException(
                            status_code=404,
                            detail=f"No event or neivethiyam name found "
                        )
                    
                    event_id=await create_unique_id(self.event_name)
                    event=Events(
                        id=event_id,
                        name=self.event_name,
                        description=self.event_description,
                        date=self.event_date,
                        start_at=self.event_start_at,
                        end_at=self.event_end_at,
                        is_special=self.is_special,
                        status=backend_enums.EventStatus.PENDING,
                        added_by=user.name,
                        updated_by=user.name
                    )

                    client=Clients(
                        name=self.client_name,
                        mobile_number=self.client_mobile_number,
                        city=self.client_city,
                        event_id=event_id
                    )

                    payment=Payments(
                        total_amount=self.total_amount,
                        paid_amount=self.paid_amount,
                        status=self.payment_status,
                        mode=self.payment_mode,
                        event_id=event_id
                    )
                        

                    combined_event_details=[event,client,payment]
                    ic("hello")
                    if is_neivethiyam_name_exists:
                        ic("be")
                  
                        event_neivethiyam=EventsNeivethiyam(
                            neivethiyam_id=self.neivethiyam_id,
                            event_id=event_id,
                            padi_kg=self.padi_kg
                        )

                        combined_event_details.append(event_neivethiyam)
                    ic("gee")
                    self.session.add_all(combined_event_details)
                    
                    self.bg_task.add_task(
                        PushNotificationCrud(
                            notify_title="New Event Added",
                            notify_body=f"{self.event_name} on {self.event_date} at {self.event_start_at}-{self.event_end_at} added-by {user.name}",
                            data_payload={
                                "screen":"event_page"
                            }
                        ).push_notification_to_all
                    )
                    
                    cur_datetime=datetime.now()
                    utc_time=datetime(
                        year=self.event_date.year,
                        month=self.event_date.month,
                        day=self.event_date.day,
                        hour=cur_datetime.hour,
                        minute=cur_datetime.minute,
                        second=cur_datetime.second
                    ).astimezone(timezone.utc)
                    return {
                        'response_msg':'successfully event added',
                        'schedule_notifications':[
                            {
                                'title':"Reminder of event assignment",
                                'body':f"Now, you can assign a workers to {event.name} on {event.date} at {event.start_at}",
                                'datetime':utc_time+timedelta(seconds=10)
                            }
                        ]
                    }

                    # return "Event added successfully"

                raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to make any changes"
                )
                
        
        except HTTPException:
            raise

        except Exception as e:
            ic(f"something went wrong while adding event details {e}")
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while adding event details {e}"
            )

class UpdateEvent(__AddEventInputs):
    async def update_event(self,event_id:str):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    await EventVerification(session=self.session).is_event_exists_by_id(event_id)
                    
                    is_event_name_exists=self.session.execute(select(EventNames.id).where(EventNames.name==self.event_name)).scalar_one_or_none()
                    
                    is_neivethiyam_name_exists=self.session.execute(select(NeivethiyamNames.id).where(NeivethiyamNames.id==self.neivethiyam_id)).scalar_one_or_none()

                    if not is_event_name_exists and not is_neivethiyam_name_exists:
                        raise HTTPException(
                            status_code=404,
                            detail="No event or neivethiyam name found"
                        )
                    
                    self.session.query(Events).filter(Events.id==event_id).update(
                        {
                            Events.name:self.event_name,
                            Events.description:self.event_description,
                            Events.date:self.event_date,
                            Events.start_at:self.event_start_at,
                            Events.end_at:self.event_end_at,
                            Events.is_special:self.is_special
                        }
                    )

                    self.session.query(Clients).filter(Clients.event_id==event_id).update(
                        {
                            Clients.name:self.client_name,
                            Clients.mobile_number:self.client_mobile_number,
                            Clients.city:self.client_city
                        }
                    )

                    self.session.query(Payments).filter(Payments.event_id==event_id).update(
                        {
                            Payments.total_amount:self.total_amount,
                            Payments.paid_amount:self.paid_amount,
                            Payments.mode:self.payment_mode,
                            Payments.status:self.payment_status
                        }
                    )
                    ic("from dbop",self.neivethiyam_id)
                    if is_neivethiyam_name_exists:
                        query_to_update=self.session.query(EventsNeivethiyam).filter(EventsNeivethiyam.event_id==event_id)
                        if query_to_update.first():
                            query_to_update.update(
                                {
                                    EventsNeivethiyam.neivethiyam_id:self.neivethiyam_id,
                                    EventsNeivethiyam.padi_kg:self.padi_kg
                                }
                            )
                        else:
                            self.session.add(
                                EventsNeivethiyam(
                                    neivethiyam_id=self.neivethiyam_id,
                                    event_id=event_id,
                                    padi_kg=self.padi_kg
                                )
                            )
                    else:
                        self.session.query(EventsNeivethiyam).filter(EventsNeivethiyam.event_id==event_id).delete()

                    return "event details updated successfully"
                raise HTTPException(
                    status_code=401,
                    detail="you are not alloed to make any changes"
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while updating event details {e}"
            )
class DeleteEvent(__DeleteEventInputs):
    async def delete_single_event(self,event_id:str):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                await EventVerification(session=self.session).is_event_exists_by_id(event_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    event=self.session.query(Events).filter(Events.id==event_id).first()
                    self.session.delete(event)
                    return "event deleted successfully"
                raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to make any changes"
                )
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while deleting event {e}"
            )
        
    async def delete_all_event(self,from_date:date,to_date:date):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    events=self.session.query(Events).filter(Events.date.between(from_date,to_date)).all()
                    for event in events:
                        self.session.delete(event)
                        
                    return f"{from_date} to {to_date} events deleted successfully"
                raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to make any changes"
                )
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while deleting event {e}"
            )

class UpdateEventCompletedStatus(__UpdateEventCompletedStatusInputs):

    async def update_previous_state_of_workers(self,prev_worker_log_query):
        if prev_worker_log_query:
            prev_worker_log=prev_worker_log_query.one_or_none()
            if prev_worker_log:
                no_of_participation=prev_worker_log.no_of_participation-1
                if no_of_participation!=0:
                    prev_worker_log_query.update(
                        {
                            WorkersParticipationLogs.no_of_participation:prev_worker_log.no_of_participation-1
                        }
                    )
                else:
                    prev_worker_log_query.delete()

    async def update_event_status(self):
        try:
            with self.session.begin():
                
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
                event=await EventVerification(session=self.session).is_event_exists_by_id(event_id=self.event_id)
                current_time=await indian_time.get_india_time()
                current_date=datetime.now().date()
                if self.event_status==backend_enums.EventStatus.COMPLETED:
                    event_status_query=self.session.query(EventsCompletedStatus).filter(EventsCompletedStatus.event_id==self.event_id)
                    event_status=event_status_query.one_or_none()
                    # ic(self.session.execute(select(EventsStatus.archagar,EventsStatus.abisegam,EventsStatus.helper,EventsStatus.poo,EventsStatus.read,EventsStatus.prepare).where(EventsStatus.event_id==self.event_id)).mappings().all())
                    # ic(self.image)
                    # ic(backend_enums.EventStatus.PENDING,backend_enums.EventStatus.PENDING.name,backend_enums.EventStatus.PENDING.value,self.event_status,event_status.image_url)
                    
                    cur_worker_names=[self.archagar,self.abisegam,self.helper,self.poo,self.read,self.prepare]
                    previous_worker_names=[EventsCompletedStatus.archagar,EventsCompletedStatus.abisegam,EventsCompletedStatus.helper,EventsCompletedStatus.poo,EventsCompletedStatus.read,EventsCompletedStatus.prepare]
                    
                    for cur_and_previous_worker_name in zip(cur_worker_names,previous_worker_names):
                        cur_worker_query=self.session.query(Workers).filter(Workers.name==cur_and_previous_worker_name[0])
                        cur_worker=cur_worker_query.one_or_none()

                        if cur_worker:
                            cur_worker_log_query=self.session.query(WorkersParticipationLogs).filter(
                                WorkersParticipationLogs.event_id==self.event_id,
                                WorkersParticipationLogs.worker_id==cur_worker.id
                            )

                            cur_worker_log=cur_worker_log_query.one_or_none()
                            
                            prev_worker_name=self.session.query(cur_and_previous_worker_name[1]).filter(EventsCompletedStatus.event_id==self.event_id).scalar()
                            prev_worker_log_query=None
                            prev_worker=None
                            if prev_worker_name:
                                prev_worker=self.session.query(Workers).filter(Workers.name==prev_worker_name).one_or_none()
                                if prev_worker:
                                    prev_worker_log_query=self.session.query(WorkersParticipationLogs).filter(WorkersParticipationLogs.event_id==self.event_id,WorkersParticipationLogs.worker_id==prev_worker.id)
                            
                            if cur_worker_log:
                                if cur_worker_log.no_of_participation!=len(cur_worker_names):

                                    #for updating cur logs and participation counts {starat}
                                    if cur_worker_log.is_reseted==False: 
                                        cur_worker_log_query.update(
                                            {
                                                WorkersParticipationLogs.no_of_participation:cur_worker_log.no_of_participation+1
                                            }
                                        )

                                        #{end} of cur

                                        #for updating prev logs and participation counts {starat}
                                        await self.update_previous_state_of_workers(
                                            prev_worker_log_query=prev_worker_log_query
                                        )
                                        #{end of previous }
                            else:
                                ic("hello",cur_worker_log)
                                query_to_check=self.session.query(WorkersParticipationLogs.id).filter(WorkersParticipationLogs.event_id==self.event_id,WorkersParticipationLogs.is_reseted==True).first()
                                ic(query_to_check)
                                if query_to_check==None:
                                    ic("hello 8")
                                    self.session.add(
                                        WorkersParticipationLogs(
                                            event_id=self.event_id,
                                            worker_id=cur_worker.id,
                                            no_of_participation=1
                                        )
                                    )
                                    #for updating prev logs and participation counts {starat}
                                    await self.update_previous_state_of_workers(
                                            prev_worker_log_query=prev_worker_log_query
                                        )
                                    #{end of previous }
                        
                        else:
                            raise HTTPException(
                                status_code=404,
                                detail="worker name not found"
                            )
                        
                    ic("lo")
                    update_dict={
                        EventsCompletedStatus.feedback:self.feedback,
                        EventsCompletedStatus.archagar:self.archagar,
                        EventsCompletedStatus.abisegam:self.abisegam,
                        EventsCompletedStatus.helper:self.helper,
                        EventsCompletedStatus.poo:self.poo,
                        EventsCompletedStatus.read:self.read,
                        EventsCompletedStatus.prepare:self.prepare,
                        EventsCompletedStatus.updated_at:current_time,
                        EventsCompletedStatus.updated_date:current_date
                    }
                    image_url=None
                    image_query_to_add=None
                    event_comp_sts_cur_id=await create_unique_id(self.event_status.value)
                    event_comp_sts_cur_query=self.session.query(EventsCompletedStatus.id).where(EventsCompletedStatus.event_id==self.event_id).scalar()
                    if event_comp_sts_cur_query:
                        ic(event_comp_sts_cur_query)
                        event_comp_sts_cur_id=event_comp_sts_cur_query
                    ic("Hello ji",event_comp_sts_cur_id)
                    # ic(self.image.file.read())
                    if self.image and not event_status:
                        image_id=await create_unique_id(self.feedback)
                        ei_to_add=EventStatusImages(
                            id=image_id,
                            image=self.image,
                            event_sts_id=event_comp_sts_cur_id
                        )
                        image_query_to_add=ei_to_add
                        
                        ic("Hello ji")
                        image_url=self.image_url_path+image_id+".jpg"
                        update_dict[EventsCompletedStatus.image_url]=image_url

                    ic(event_status)
                    if event_status:
                        ic(event_status.image_url)
                        if self.image and event_status.image_url:
                            
                            self.session.query(EventStatusImages).filter(EventStatusImages.event_sts_id==event_status.id).update(
                                {
                                    EventStatusImages.image:self.image
                                }
                            )

                            image_url=event_status.image_url

                        
                        event_status_query.update(
                            update_dict
                        )

                    else:
                        ic("ulla yeahh veliyav")
                        event_sts_to_add=EventsCompletedStatus(
                            id=event_comp_sts_cur_id,
                            event_id=self.event_id,
                            feedback=self.feedback,
                            archagar=self.archagar,
                            abisegam=self.abisegam,
                            helper=self.helper,
                            poo=self.poo,
                            read=self.read,
                            prepare=self.prepare,
                            updated_at=current_time,
                            updated_date=current_date,
                            image_url=image_url
                        )

                        
                        quries_to_add=[event_sts_to_add]
                        if image_query_to_add:
                            quries_to_add.append(image_query_to_add)
                        self.session.add_all(quries_to_add)  

                    self.session.query(Events).filter(Events.id==self.event_id).update(
                        {
                            Events.status:self.event_status,
                            Events.updated_by:user.name
                        }
                    )

                    self.session.query(EventsPendingCanceledStatus).filter(EventsPendingCanceledStatus.event_id==self.event_id).delete()
                    self.session.query(EventsAssignments).filter(EventsAssignments.event_id==self.event_id).update({EventsAssignments.is_completed:True})
                    ic("event completed status updated successfully")

                    # ["fUKAXNhpQHCOiuFfHT8PQ-:APA91bEYqkU1qtNyE5UDeqDyi1bgI9Rfmqm1bvg2u6IJm5wgngmCjW9M0LWibAdjfY6G6OrEO0qwLrFb9cI6tVN2NafT4h-KDn2gd_1a6BPgxiFn07nbrC4"]
                    
                    ic(image_url)
                    compressed_image_url=await notification_image_url.get_notification_image_url(
                        session=self.session,
                        request=self.request,
                        notification_title="event status updated - completed",
                        notification_image=self.image,
                        compress_image=True
                       
                    )
                    ic(compressed_image_url)
                    self.bg_task.add_task(
                        PushNotificationCrud(
                            notify_title="event status updated - completed".title(),
                            notify_body=f"{event.name} completed on {current_date} at {current_time} updated-by {user.name}".title(),
                            data_payload={
                                "screen":"event_page"
                            }
                        ).push_notification_to_all,
                        image_url=compressed_image_url
                    )
                    return
                
                # raise HTTPException(
                #     status_code=404,
                #     detail=f"invalid event status {self.event_status.value}"
                # )
                ic(f"404 : invalid event status {self.event_status.value}")
                send_error_notification(
                    user_id=self.user_id,
                    error_title="invalid event status : 404".title(),
                    error_body=f"for {event.name} expected status 'completed' actual '{self.event_status.value}'".title,
                    notify_data_payload={
                        "screen":"home_screen"
                    }
                )
                   

        except Exception as e:
            ic(f"500 : something went wrong while updating event completed status {e}")
            send_error_notification(
                    user_id=self.user_id,
                    error_title="error updateing event status : 500".title(),
                    error_body=f"for {event.name} Something went wrong, Please Try Again".title(),
                    notify_data_payload={
                        "screen":"home_screen"
                    }
                )
            # raise HTTPException(
            #     status_code=500,
            #     detail=f"something went wrong while updating event completed status {e}"
            # )

class UpdateEventPendingCanceledStatus(__UpdateEventPendingCanceledInputs):
    async def update_event_status(self):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
                event=await EventVerification(session=self.session).is_event_exists_by_id(event_id=self.event_id)
                event_status_query=self.session.query(EventsCompletedStatus).filter(EventsCompletedStatus.event_id==self.event_id)
                event_status=event_status_query.one_or_none()

                current_time=await indian_time.get_india_time()
                current_date=datetime.now().date()

                if self.event_status==backend_enums.EventStatus.CANCELED or self.event_status==backend_enums.EventStatus.PENDING:
                    print("hi from")
                    if event_status:
                        self.session.delete(event_status)
                        self.session.query(WorkersParticipationLogs).filter(WorkersParticipationLogs.event_id==self.event_id,WorkersParticipationLogs.is_reseted==False).delete()
                    
                    event_pen_canc_sts_query=self.session.query(EventsPendingCanceledStatus).filter(EventsPendingCanceledStatus.event_id==self.event_id)
                    if not event_pen_canc_sts_query.one_or_none():
                        add_desc=EventsPendingCanceledStatus(
                            description=self.description,
                            event_id=self.event_id,
                            updated_at=current_time,
                            updated_date=current_date
                        )

                        self.session.add(add_desc)
                    
                    else:
                        event_pen_canc_sts_query.update(
                            {
                                EventsPendingCanceledStatus.description:self.description,
                                EventsPendingCanceledStatus.updated_at:current_time,
                                EventsPendingCanceledStatus.updated_date:current_date
                            }
                        )

                    self.session.query(Events).filter(Events.id==self.event_id).update(
                        {
                            Events.status:self.event_status,
                            Events.updated_by:user.name
                        }
                    )
                    self.session.query(EventsAssignments).filter(EventsAssignments.event_id==self.event_id).update({EventsAssignments.is_completed:False})
                    ic(f"successfully event {self.event_status.value} status updated")
                    self.bg_task.add_task(
                        PushNotificationCrud(
                            notify_title=f"event status updated - {self.event_status.value}".title(),
                            notify_body=f"{event.name} on {current_date} at {current_time} updated-by {user.name}".title(),
                            data_payload={
                                "screen":"event_page"
                            }
                        ).push_notification_to_all
                    )
                    return
                # raise HTTPException(
                #     status_code=404,
                #     detail=f"invalid event status {self.event_status.value}"
                # )
                ic(f"404 : invalid event status {self.event_status.value}")
                send_error_notification(
                    user_id=self.user_id,
                    error_title="invalid event status".title(),
                    error_body=f"for {event.name} expected status 'pending or canceled' actual '{self.event_status.value}'".title,
                    notify_data_payload={
                        "screen":"home_screen"
                    }
                )


        except Exception as e:
            print(f"something went wrong while updating event {self.event_status.value} status {e}")
            send_error_notification(
                    user_id=self.user_id,
                    error_title="error updateing event status : 500".title(),
                    error_body=f"for {event.name} something went wrong, please try again".title,
                    notify_data_payload={
                        "screen":"home_screen"
                    }
                )
            # raise HTTPException(
            #     status_code=500,
            #     detail=f"something went wrong while updating event {self.event_status.value} status {e}"
            # )
        
class GetEventStatusImage:
    def __init__(self,session:Session,image_id:str):
        self.session=session
        self.image_id=image_id
    async def get_image(self):
        try:
            image=self.session.query(EventStatusImages).filter(EventStatusImages.id==self.image_id).first()
            if image:
                return image.image
            raise HTTPException(
                status_code=404,
                detail="image not found"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while fetching image {e}"
            )

class ContactDescription(__ContactDescriptionInputs):

    async def add_description(self,event_id:str,contact_description:str):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                await EventVerification(session=self.session).is_event_exists_by_id(event_id=event_id)
                query_to_add_update=self.session.query(EventsContactDescription).filter(EventsContactDescription.event_id==event_id)
                if not query_to_add_update.one_or_none():
                    cont_desc=EventsContactDescription(
                        description=contact_description,
                        event_id=event_id,
                        updated_by=user.name,
                        updated_date=datetime.now().date(),
                        updated_at=await indian_time.get_india_time()
                    )

                    self.session.add(cont_desc)

                    return JSONResponse(
                        status_code=201,
                        content="call description added successfully"
                    )
                
                else:
                    query_to_add_update.update(
                        {
                            EventsContactDescription.description:contact_description,
                            EventsContactDescription.updated_by:user.name,
                            EventsContactDescription.updated_date:datetime.now().date(),
                            EventsContactDescription.updated_at:await indian_time.get_india_time()
                        }
                    )

                    return JSONResponse(
                        status_code=200,
                        content="call description updated successfully"
                    )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while adding contact description {e}"
            )
        
    async def delete_description(self,contact_desc_id:int):
        try:
            with self.session.begin():
                await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                query_to_del=self.session.query(EventsContactDescription).filter(EventsContactDescription.id==contact_desc_id)
                if query_to_del.one_or_none():
                    query_to_del.delete()

                    return "contact description deleted successfully"
                
                raise HTTPException(
                    status_code=404,
                    detail=f"contact description not found"
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="something went wrong while deleting contact description {e}"
            )
        
    async def get_description(self,event_id:str):
        try:
            with self.session.begin():
                await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                await EventVerification(session=self.session).is_event_exists_by_id(event_id=event_id)

                query_to_get=self.session.execute(
                    select(
                        EventsContactDescription.id,
                        EventsContactDescription.description,
                        EventsContactDescription.updated_by,
                        EventsContactDescription.updated_at,
                        EventsContactDescription.updated_date
                    ).where(
                        EventsContactDescription.event_id==event_id
                    )
                ).mappings().all()
                

                return query_to_get
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="something went wrong while deleting contact description {e}"
            )
                    

class EventAssignmentCrud:
    def __init__(self,session:Session,user_id:str):
        self.session=session
        self.user_id=user_id

    async def add_update_event_assignment(
        self,
        bg_task:BackgroundTasks,
        event_id:str,
        assigned_archagar:str,
        assigned_abisegam:str,
        assigned_helper:str,
        assigned_poo:str,
        assigned_read:str,
        assigned_prepare:str,
    ):
        try:
            with self.session.begin():
                cur_datetime_utc=datetime.now(timezone.utc)
                user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)
                event=await EventVerification(self.session).is_event_exists_by_id(event_id)

                role_names = {
                    "archagar": assigned_archagar,
                    "abisegam": assigned_abisegam,
                    "helper": assigned_helper,
                    "poo": assigned_poo,
                    "read": assigned_read,
                    "prepare": assigned_prepare
                }
                ic(role_names)
                workers=list(set(role_names.values()))
                
                if user.role==backend_enums.UserRole.ADMIN:
                    checked_workers=self.session.execute(select(Workers.id,Workers.user_id).where(Workers.name.in_(workers))).mappings().all()
                    ic(checked_workers)
                    if len(workers)==len(checked_workers):
                        event_assign_query=self.session.query(EventsAssignments).filter(EventsAssignments.event_id==event_id)
                        notify_title="Event Assignment".title()
                        notify_body=f"You are assigned to a event of {event.name} on {event.date} at {event.start_at}".title()
                        if not event_assign_query.one_or_none():
                            event_assignment=EventsAssignments(
                                event_id=event_id,
                                archagar=assigned_archagar,
                                abisegam=assigned_abisegam,
                                helper=assigned_helper,
                                poo=assigned_poo,
                                read=assigned_read,
                                prepare=assigned_prepare,
                                assigned_by=user.name,
                                assigned_datetime=cur_datetime_utc,
                                is_completed=False
                            )

                            self.session.add(event_assignment)
                            
                            for worker in checked_workers:
                                worker_user_id=worker['user_id']
                                if worker_user_id:
                                    await NotificationsCrud(
                                        session=self.session,
                                        user_id=user.id,
                                        is_for=worker_user_id
                                    ).add_notification(
                                        notify_title=notify_title,
                                        notify_body=notify_body
                                    )
                                    order_dict=FirebaseCrud(user_id=worker_user_id).get_fcm_tokens()
                                    ic(order_dict)
                                    if order_dict:
                                        bg_task.add_task(
                                            PushNotificationCrud(
                                                notify_title=notify_title,
                                                notify_body=notify_body,
                                                data_payload={
                                                    "screen":"home_screen"
                                                }
                                            ).push_notifications_individually,
                                            fcm_tokens=order_dict
                                        )
                            return f"Successfully workers assigned to {event.name}"
                        else:
                            event_assign_query.update(
                                {
                                    EventsAssignments.archagar:assigned_archagar,
                                    EventsAssignments.abisegam:assigned_abisegam,
                                    EventsAssignments.helper:assigned_helper,
                                    EventsAssignments.poo:assigned_poo,
                                    EventsAssignments.read:assigned_read,
                                    EventsAssignments.prepare:assigned_prepare,
                                    EventsAssignments.assigned_by:user.name,
                                    EventsAssignments.assigned_datetime:cur_datetime_utc 
                                }
                            )

                            for worker in checked_workers:
                                worker_user_id=worker['user_id']
                                if worker_user_id:
                                    await NotificationsCrud(
                                        session=self.session,
                                        user_id=user.id,
                                        is_for=worker_user_id
                                    ).add_notification(
                                        notify_title=notify_title,
                                        notify_body=notify_body
                                    )
                                    order_dict=FirebaseCrud(user_id=worker_user_id).get_fcm_tokens()
                                    ic(order_dict)
                                    if order_dict:
                                        bg_task.add_task(
                                            PushNotificationCrud(
                                                notify_title=notify_title,
                                                notify_body=notify_body,
                                                data_payload={
                                                    "screen":"home_screen"
                                                }
                                            ).push_notifications_individually,
                                            fcm_tokens=order_dict
                                        )

                            return f"Successfully workers assignment updated for {event.name}"
                    
                    raise HTTPException(
                        status_code=404,
                        detail="worker name not found"
                    )
                raise HTTPException(
                    status_code=401,
                    detail="You are not allowed to make any changes"
                )
            
        except HTTPException:
            raise

        except Exception as e:
            ic(f"Something went wrong while assigning worker to event : {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Something went wrong while assigning worker to event : {e}"
            )
    
    async def delete_event_assignment(self,event_id):
        try:
            with self.session.begin():
                user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)
                await EventVerification(self.session).is_event_exists_by_id(event_id)

                if user.role==backend_enums.UserRole.ADMIN:
                    self.session.query(EventsAssignments).filter(EventsAssignments.event_id==event_id).delete()

                    return "assigned event deleteed successfully"
                
                raise HTTPException(
                    status_code=401,
                    detail="You are not allowed to make any changes"
                )
        except HTTPException:
            raise
        except Exception as e:
            ic(f"something went wrong while deleting Assinged event")
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while deleting Assinged event"
            )
    
    async def get_assigned_events(self,worker_name:Optional[str]=None):
        try:
            user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
            if worker_name==None:
                worker_name=self.session.execute(select(Workers.name).where(Workers.user_id==user.id)).scalar_one_or_none()
            ic(worker_name)
            if worker_name:
                assigned_events=self.session.execute(
                    select(
                        EventsAssignments.assigned_datetime,
                        EventsAssignments.assigned_by,
                        Events.id.label("event_id"),
                        Events.name.label('event_name'),
                        Events.date.label("event_date"),
                        Events.start_at.label("event_start_at")
                    )
                    .join(Events,Events.id==EventsAssignments.event_id,isouter=True)
                    .where(
                        and_(
                            or_(
                                EventsAssignments.archagar==worker_name,
                                EventsAssignments.abisegam==worker_name,
                                EventsAssignments.prepare==worker_name,
                                EventsAssignments.poo==worker_name,
                                EventsAssignments.read==worker_name,
                                EventsAssignments.helper==worker_name
                            ),
                            EventsAssignments.is_completed==False
                        )
                    )
                    .order_by(Events.date)
                ).mappings().all()

                return {"assigned_events":assigned_events}
            raise HTTPException(
                status_code=404,
                detail="Worker not using the app"
            )
        except HTTPException:
            raise
        except Exception as e:
            ic(f"something went wrong while getting assigned events {e}")
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while getting assigned events {e}"
            )