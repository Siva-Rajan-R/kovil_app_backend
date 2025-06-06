from database.models.event import (
    Events,Clients,Payments,EventsCompletedStatus,EventsPendingCanceledStatus,EventNames,EventStatusImages,NeivethiyamNames,EventsNeivethiyam,EventsContactDescription
)
from database.models.workers import Workers,WorkersParticipationLogs
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select,func,desc
from enums import backend_enums
from security.uuid_creation import create_unique_id
from datetime import date,time
from pydantic import EmailStr
from fastapi.exceptions import HTTPException
from database.operations.user_auth import UserVerification
from typing import Optional
from utils import indian_time
from datetime import datetime
from icecream import ic
from utils.push_notification import PushNotificationCrud
from firebase_db.operations import FirebaseCrud

class __AddEventInputs:
    def __init__(
            self,
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
            image_url_path:str
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

class __UpdateEventPendingCanceledInputs:
    def __init__(
        self,
        session:Session,
        user_id:str,
        event_id:str,
        event_status:backend_enums.EventStatus,
        description:str
    ):
        self.session=session
        self.user_id=user_id
        self.event_id=event_id
        self.event_status=event_status
        self.description=description

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
                    added_event_name=EventNames(
                        name=event_name,
                        amount=event_amount,
                        is_special=is_special
                    )
                    self.session.add(added_event_name)
                    return "successfully event name added"
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
        
    async def delete_event_name_and_amount(self,event_name_id):
        try:
            with self.session.begin():
                user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    en_to_delete=self.session.query(EventNames).filter(EventNames.id==event_name_id).first()
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
                    added_event_name=NeivethiyamNames(
                        name=neivethiyam_name,
                        amount=neivethiyam_amount
                    )
                    self.session.add(added_event_name)
                    return "successfully neivethiyam name added"
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
        
    async def delete_neivethiyam_name_and_amount(self,neivethiyam_name_id):
        try:
            with self.session.begin():
                user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    nv_to_delete=self.session.query(NeivethiyamNames).filter(NeivethiyamNames.id==neivethiyam_name_id).first()
                    if nv_to_delete:
                        self.session.delete(nv_to_delete)
                    else:
                        raise HTTPException(
                            status_code=404,
                            detail="neivethiyam id not found"
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
                    
                    is_neivethiyam_name_exists=self.session.execute(select(NeivethiyamNames.id).where(NeivethiyamNames.id==self.neivethiyam_id)).scalar_one_or_none()
                    ic(is_event_name_exists,is_neivethiyam_name_exists)
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

                    return "successfully event added"

                raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to make any changes"
                )
                
        
        except HTTPException:
            raise

        except Exception as e:
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
                        EventsCompletedStatus.updated_at:await indian_time.get_india_time(),
                        EventsCompletedStatus.updated_date:datetime.now().date()
                    }
                    image_url=None
                    image_query_to_add=None
                    event_comp_sts_cur_id=1
                    event_comp_sts_cur_query=self.session.query(EventsCompletedStatus.id).order_by(desc(EventsCompletedStatus.id)).first()
                    if event_comp_sts_cur_query:
                        ic(event_comp_sts_cur_query)
                        event_comp_sts_cur_id=event_comp_sts_cur_query[0]+1
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
                        image_url=self.image_url_path+image_id
                        update_dict[EventsCompletedStatus.image_url]=image_url

                    elif self.image and event_status.image_url:
                        
                        self.session.query(EventStatusImages).filter(EventStatusImages.event_sts_id==event_status.id).update(
                            {
                                EventStatusImages.image:self.image
                            }
                        )

                    if event_status:
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
                            updated_at=await indian_time.get_india_time(),
                            updated_date=datetime.now().date(),
                            image_url=image_url
                        )

                        self.session.add(event_sts_to_add)
                        if image_query_to_add:
                            self.session.add(image_query_to_add)

                    self.session.query(Events).filter(Events.id==self.event_id).update(
                        {
                            Events.status:self.event_status,
                            Events.updated_by:user.name
                        }
                    )

                    self.session.query(EventsPendingCanceledStatus).filter(EventsPendingCanceledStatus.event_id==self.event_id).delete()
                    ic("event completed status updated successfully")

                    # ["fUKAXNhpQHCOiuFfHT8PQ-:APA91bEYqkU1qtNyE5UDeqDyi1bgI9Rfmqm1bvg2u6IJm5wgngmCjW9M0LWibAdjfY6G6OrEO0qwLrFb9cI6tVN2NafT4h-KDn2gd_1a6BPgxiFn07nbrC4"]
                    fcm_tokens=FirebaseCrud(user.mobile_number).get_fcm_tokens()
                    if fcm_tokens:
                        await PushNotificationCrud(
                            notify_title="event completed status updated successfully".title(),
                            notify_body=f"for {event.name}".title(),
                            data_payload={
                                "screen":"event_page"
                            }
                        ).push_notifications_individually(fcm_tokens=fcm_tokens)
                    return
                raise HTTPException(
                    status_code=404,
                    detail=f"invalid event status {self.event_status.value}"
                )
            
        except HTTPException:
            raise

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while updating event completed status {e}"
            )

class UpdateEventPendingCanceledStatus(__UpdateEventPendingCanceledInputs):
    async def update_event_status(self):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
                event=await EventVerification(session=self.session).is_event_exists_by_id(event_id=self.event_id)
                event_status_query=self.session.query(EventsCompletedStatus).filter(EventsCompletedStatus.event_id==self.event_id)
                event_status=event_status_query.one_or_none()

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
                            updated_at=await indian_time.get_india_time(),
                            updated_date=datetime.now().date()
                        )

                        self.session.add(add_desc)
                    
                    else:
                        event_pen_canc_sts_query.update(
                            {
                                EventsPendingCanceledStatus.description:self.description,
                                EventsPendingCanceledStatus.updated_at:await indian_time.get_india_time(),
                                EventsPendingCanceledStatus.updated_date:datetime.now().date()
                            }
                        )

                    self.session.query(Events).filter(Events.id==self.event_id).update(
                        {
                            Events.status:self.event_status,
                            Events.updated_by:user.name
                        }
                    )

                    ic(f"successfully event {self.event_status.value} status updated")
                
                    await PushNotificationCrud(
                            notify_title=f"successfully event {self.event_status.value} status updated".title(),
                            notify_body=f"for {event.name}".title(),
                            data_payload={
                                "screen":"event_page"
                            }
                    ).push_notifications_individually(["fUKAXNhpQHCOiuFfHT8PQ-:APA91bEYqkU1qtNyE5UDeqDyi1bgI9Rfmqm1bvg2u6IJm5wgngmCjW9M0LWibAdjfY6G6OrEO0qwLrFb9cI6tVN2NafT4h-KDn2gd_1a6BPgxiFn07nbrC4"])

                    return
                raise HTTPException(
                    status_code=404,
                    detail=f"invalid event status {self.event_status.value}"
                )

        
        except HTTPException:
            raise

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while updating event {self.event_status.value} status {e}"
            )
        
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
                    
