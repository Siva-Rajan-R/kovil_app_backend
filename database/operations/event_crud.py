from database.models.event import (
    Events,Clients,Payments,EventsCompletedStatus,EventsPendingCanceledStatus,EventNames,EventStatusImages,NeivethiyamNames,EventsNeivethiyam,EventsContactDescription,EventsAssignments
)
from database.models.workers import Workers,WorkersParticipationLogs
from database.main import SessionLocal
from fastapi import BackgroundTasks,Request,File,UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,desc,or_,and_,update,delete
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
from redis_db.redis_crud import RedisCrud
from redis_db.redis_etag_keys import WORKER_ETAG_KEY,WORKER_WITH_USER_ETAG_KEY
import asyncio
from collections import Counter

class __AddEventInputs:
    def __init__(
            self,
            bg_task:BackgroundTasks,
            session:AsyncSession,
            user_id:str,
            event_name:str,
            event_description:str,
            event_date:date,
            event_start_at:str,
            event_end_at:str,
            client_name:str,
            client_mobile_number:str,
            client_city:str,
            total_amount:float,
            paid_amount:float,
            payment_status:backend_enums.PaymetStatus,
            payment_mode:backend_enums.PaymentMode,
            neivethiyam_id:Optional[int]=None,
            is_special:Optional[bool]=None,
            padi_kg:Optional[float]=None
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
    def __init__(self,session:AsyncSession,user_id:str):
        self.session=session
        self.user_id=user_id

class __DeleteEventInputs:
    def __init__(self,session:AsyncSession,user_id:str):
        self.session=session
        self.user_id=user_id

class __UpdateEventCompletedStatusInputs:
    def __init__(
            self,
            session:AsyncSession,
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
        session:AsyncSession,
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
    def __init__(self,session:AsyncSession,user_id:str):
        self.session=session
        self.user_id=user_id

class EventVerification:
    def __init__(self,session:AsyncSession):
        self.session=session

    async def is_event_exists_by_id(self,event_id:str):
        event=(await self.session.execute(select(Events).where(Events.id==event_id))).scalar_one_or_none()
        if event:
            return event
        raise HTTPException(
            status_code=404,
            detail="event not found"
        )
    
class NeivethiyamNameVerification:
    def __init__(self,session:AsyncSession):
        self.session=session
    
    async def is_neivethiyam_exists_by_id(self,neivethiyam_id):
        neivethiyam_id=(await self.session.execute(select(NeivethiyamNames.id).where(NeivethiyamNames.id==neivethiyam_id))).scalar_one_or_none()
        if neivethiyam_id:
            return neivethiyam_id
        raise HTTPException(
            status_code=404,
            detail="neivethiyam id not found"
        )
    
    async def is_neivethiyam_exists_by_name(self,neivethiyam_name):
        neivethiyam_id=(await self.session.execute(select(NeivethiyamNames.id).where(NeivethiyamNames.name==neivethiyam_name))).scalar_one_or_none()
        if neivethiyam_id:
            return neivethiyam_id
        raise HTTPException(
            status_code=404,
            detail="neivethiyam id not found"
        )
    
class EventNameVerification:
    def __init__(self,session:AsyncSession):
        self.session=session
    
    async def is_event_name_exists_by_id(self,event_name_id):
        event_name_id=(await self.session.execute(select(EventNames.id).where(EventNames.id==event_name_id))).scalar_one_or_none()
        if event_name_id:
            return event_name_id
        raise HTTPException(
            status_code=404,
            detail="event name id not found"
        )
    
    async def is_event_name_exists_by_name(self,event_name):
        event_name_id=(await self.session.execute(select(EventNames.id).where(EventNames.name==event_name))).scalar_one_or_none()
        if event_name_id:
            return event_name_id
        raise HTTPException(
            status_code=404,
            detail="event name not found"
        )


class EventNameAndAmountCrud(__EventAndNeivethiyamNameAndAmountCrudInputs):
    async def add_event_name_and_amt(self,event_name:str,event_amount:int,is_special:bool):
        try:
            async with self.session.begin():
                user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    is_event_name_exists=(await self.session.execute(select(EventNames.name).where(EventNames.name==event_name))).scalar_one_or_none()
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
            ic(detail="something went wrong while adding event name")
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while adding event name {e}"
            )
        
    async def delete_event_name_and_amount(self,event_name):
        try:
            async with self.session.begin():
                user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:

                    en_to_delete=delete(EventNames).where(EventNames.name==event_name).returning(EventNames.name)
                    result = await self.session.execute(en_to_delete)

                    if not result.scalar_one_or_none():
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
                event_names=(await self.session.execute(
                    select(
                        EventNames.id,
                        EventNames.name,
                        EventNames.amount,
                        EventNames.is_special
                    )
                    .order_by(desc(EventNames.id))
                )).mappings().all()

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
            async with self.session.begin():
                user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    is_neivethiyam_name_exists=(await self.session.execute(select(NeivethiyamNames.name).where(NeivethiyamNames.name==neivethiyam_name))).scalar_one_or_none()
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
            async with self.session.begin():
                user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    nv_to_delete=delete(NeivethiyamNames).where(NeivethiyamNames.name==neivethiyam_name).returning(NeivethiyamNames.name)
                    result = await self.session.execute(nv_to_delete)
                    if not result.scalar_one_or_none():
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
                neivethiyam_names=(await self.session.execute(
                    select(
                        NeivethiyamNames.id,
                        NeivethiyamNames.name,
                        NeivethiyamNames.amount
                    )
                    .order_by(desc(NeivethiyamNames.id))
                )).mappings().all()

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
            async with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:

                    await EventNameVerification(session=self.session).is_event_name_exists_by_name(self.event_name)
                    is_neivethiyam_name_exists=None
                    if self.neivethiyam_id:
                        await NeivethiyamNameVerification(session=self.session).is_neivethiyam_exists_by_id(self.neivethiyam_id)

                    
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
                    # for deleting etag from redis
                    keys_to_del=[
                        f"event-calendar-{self.event_date.month}-{self.event_date.year}-etag",
                        f"events-{self.event_date}-etag"
                    ]
                    await RedisCrud(key="").unlink_etag_from_redis(*keys_to_del)
                    # 
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
            async with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    await EventVerification(session=self.session).is_event_exists_by_id(event_id)
                    
                    await EventNameVerification(session=self.session).is_event_name_exists_by_name(self.event_name)
                    is_neivethiyam_id_exists=None
                    if self.neivethiyam_id:
                        is_neivethiyam_id_exists=await NeivethiyamNameVerification(session=self.session).is_neivethiyam_exists_by_id(self.neivethiyam_id)
                
                    update_event=update(Events).where(Events.id==event_id).values(
                        name=self.event_name,
                        description=self.event_description,
                        date=self.event_date,
                        start_at=self.event_start_at,
                        end_at=self.event_end_at,
                        is_special=self.is_special
                    )

                    update_client=update(Clients).where(Clients.event_id==event_id).values(
                        name=self.client_name,
                        mobile_number=self.client_mobile_number,
                        city=self.client_city
                    )

                    update_payment=update(Payments).where(Payments.event_id==event_id).values(
                        total_amount=self.total_amount,
                        paid_amount=self.paid_amount,
                        mode=self.payment_mode,
                        status=self.payment_status
                    )
                    for update_query in [update_event,update_client,update_payment]:
                        await self.session.execute(update_query)

                    ic("from dbop",self.neivethiyam_id,self.padi_kg)
                    if is_neivethiyam_id_exists:
                        
                        query_to_update=update(EventsNeivethiyam).where(EventsNeivethiyam.event_id==event_id).values(
                            neivethiyam_id=self.neivethiyam_id,
                            padi_kg=self.padi_kg
                        ).returning(EventsNeivethiyam.id)

                        result=await self.session.execute(query_to_update)

                        if not result.scalar_one_or_none():
                            self.session.add(
                                EventsNeivethiyam(
                                    neivethiyam_id=self.neivethiyam_id,
                                    event_id=event_id,
                                    padi_kg=self.padi_kg
                                )
                            )
                    else:
                        await self.session.execute(delete(EventsNeivethiyam).where(EventsNeivethiyam.event_id==event_id))
                    # for deleting redis etag
                    await RedisCrud(key=f"events-{self.event_date}-etag").unlink_etag_from_redis()
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
            async with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    event_to_del=delete(Events).where(Events.id==event_id).returning(Events.date)
                    result=await self.session.execute(event_to_del)
                    event_date=result.scalar_one_or_none()
                    if event_date:
                        # for deleting redis etag key
                        keys_to_del=[
                            f"event-calendar-{event_date.month}-{event_date.year}-etag",
                            f"events-{event_date}-etag"
                        ]
                        await RedisCrud(key="").unlink_etag_from_redis(*keys_to_del)
                        # 
                        return "Event deleted successfully"
                    raise HTTPException(
                        status_code=404,
                        detail="Event id not found"
                    )
                
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
            async with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    events_to_del=delete(Events).where(Events.date.between(from_date,to_date))
                    await self.session.execute(events_to_del)
                    # reids etag delete
                    etag_keys_to_del = [
                        keys
                        for i in range((to_date - from_date).days + 1)
                        for keys in [
                            f"events-{(from_date + timedelta(days=i))}-etag",
                            f"event-calendar-{(from_date + timedelta(days=i)).month}-{(from_date + timedelta(days=i)).year}-etag"
                        ]
                    ]
                    await RedisCrud(key="").unlink_etag_from_redis(*etag_keys_to_del)
                    # 
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

    async def update_event_status(self):
        try:
            async with self.session.begin():

                if self.event_status==backend_enums.EventStatus.COMPLETED:
                    user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
                    event=await EventVerification(session=self.session).is_event_exists_by_id(event_id=self.event_id)
                    current_time=await indian_time.get_india_time()
                    current_date=datetime.now().date()
                    event_comp_sts_cur_id=await create_unique_id(data=event.name)

                    event_to_update=update(EventsCompletedStatus).where(EventsCompletedStatus.event_id==self.event_id).values(
                        feedback=self.feedback,
                        archagar=self.archagar,
                        abisegam=self.abisegam,
                        helper=self.helper,
                        poo=self.poo,
                        read=self.read,
                        prepare=self.prepare,
                        updated_at=current_time,
                        updated_date=current_date
                    ).returning(EventsCompletedStatus.id)

                    updated_result=(await self.session.execute(event_to_update)).scalar_one_or_none()
                    ic(updated_result)
                    if not updated_result:
                        image_url=None

                        if self.image:
                            image_id=await create_unique_id(data=event.name)
                            image_url=self.image_url_path+image_id
                            
                            self.session.add(
                                EventStatusImages(
                                    id=image_id,
                                    image=self.image,
                                    event_sts_id=event_comp_sts_cur_id
                                )
                            )

                        self.session.add(
                            EventsCompletedStatus(
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
                        )
                    else:
                        if self.image:
                            result=await self.session.execute(
                                update(EventStatusImages).where(EventStatusImages.event_sts_id==updated_result).values(
                                    image=self.image
                                )
                            )
                            if result.rowcount==0:
                                image_id=await create_unique_id(data=event.name)
                                self.session.add(
                                    EventStatusImages(
                                        id=image_id,
                                        image=self.image,
                                        event_sts_id=updated_result
                                    )
                                )
                                await self.session.execute(update(EventsCompletedStatus).where(EventsCompletedStatus.event_id==self.event_id).values(image_url=self.image_url_path+image_id))
                        else:
                            await self.session.execute(
                                delete(EventStatusImages).where(EventStatusImages.event_sts_id==updated_result)
                            )
                            await self.session.execute(
                                update(EventsCompletedStatus).where(EventsCompletedStatus.event_id==self.event_id).values(image_url=None)
                            )

                    await self.session.execute(update(Events).where(Events.id==self.event_id).values(updated_by=user.name,status=backend_enums.EventStatus.COMPLETED))
                    await self.session.execute(delete(EventsPendingCanceledStatus).where(EventsPendingCanceledStatus.event_id==self.event_id))

                    workers=[self.archagar,self.abisegam,self.helper,self.poo,self.read,self.prepare]
                    workers_counts=Counter(workers)
                    ic(workers_counts)
                    workers_with_id=(await self.session.execute(select(Workers.name,Workers.id).where(Workers.name.in_(list(workers_counts.keys()))))).mappings().all()
                    ic(workers_with_id)
                    if (len(workers_counts)==len(workers_with_id) and (workers_counts!=[] and workers_with_id!=[])):
                        ic("entered")
                        is_reseted=(await self.session.execute(select(WorkersParticipationLogs.is_reseted).where(WorkersParticipationLogs.event_id==self.event_id))).first()
                        if is_reseted!=None:
                            is_reseted=is_reseted[0]
                        ic(is_reseted)
                        if is_reseted!=True:
                            await self.session.execute(delete(WorkersParticipationLogs).where(WorkersParticipationLogs.event_id==self.event_id))
                            ic(workers_with_id)
                            for worker in workers_with_id:
                                ic(worker)
                                name=worker['name']
                                id=worker['id']
                                ic(worker,id)
                                self.session.add(
                                    WorkersParticipationLogs(
                                        event_id=self.event_id,
                                        worker_id=id,
                                        no_of_participation=workers_counts[name],
                                        is_reseted=False
                                    )
                                )
                    else:
                        raise HTTPException(
                            status_code=404,
                            detail=f"for {event.name}, invalid worker name"
                        )
                    
                    # redis etag deletion
                    etag_to_del=[
                        f"events-{event.date}-etag",
                        WORKER_WITH_USER_ETAG_KEY
                    ]
                    await RedisCrud(key='').unlink_etag_from_redis(*etag_to_del)
                    # 

                    if self.image:  
                        compressed_image_url=await notification_image_url.get_notification_image_url(
                            session=self.session,
                            request=self.request,
                            notification_title="event status updated - completed",
                            notification_image=self.image,
                            compress_image=True
                        
                        )
                        ic(compressed_image_url)
                        asyncio.create_task(
                            PushNotificationCrud(
                                notify_title="event status updated - completed".title(),
                                notify_body=f"{event.name} completed on {current_date} at {current_time} updated-by {user.name}".title(),
                                data_payload={
                                    "screen":"event_page"
                                }
                            ).push_notification_to_all(image_url=compressed_image_url)
                        )

                    
                    

                    return "event completed sts updated successfully"
                
                raise HTTPException(
                    status_code=404,
                    detail=f"invalid event status, expected status 'completed' actual '{self.event_status.value}'"
                )
                
                
                   
        except HTTPException as httpe:
            ic(f"{httpe.status_code}: {httpe.detail}")
            await send_error_notification(
                user_id=self.user_id,
                error_title=f"error updating event status : {httpe.status_code}".title(),
                error_body=httpe.detail.title(),
                notify_data_payload={
                    "screen":"home_screen"
                }
            )

        except Exception as e:
            ic(f"500 : something went wrong while updating event completed status {e}")
            await send_error_notification(
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
            async with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
                event=await EventVerification(session=self.session).is_event_exists_by_id(event_id=self.event_id)
                event_status_to_del=delete(EventsCompletedStatus).where(EventsCompletedStatus.event_id==self.event_id).returning(EventsCompletedStatus.id)
                event_sts_del_result = await self.session.execute(event_status_to_del)

                current_time=await indian_time.get_india_time()
                current_date=datetime.now().date()

                if self.event_status==backend_enums.EventStatus.CANCELED or self.event_status==backend_enums.EventStatus.PENDING:
                    print("hi from")
                    if event_sts_del_result.scalar_one_or_none():
                        await self.session.execute(delete(WorkersParticipationLogs).where(WorkersParticipationLogs.event_id==self.event_id,WorkersParticipationLogs.is_reseted==False))
                    ic("vanakam da")
                    event_pen_canc_sts_toupdate=update(EventsPendingCanceledStatus).where(EventsPendingCanceledStatus.event_id==self.event_id).values(
                        description=self.description,
                        updated_at=current_time,
                        updated_date=current_date
                    ).returning(EventsPendingCanceledStatus.id)

                    event_pen_canc_sts_upt_result = await self.session.execute(event_pen_canc_sts_toupdate)

                    if not event_pen_canc_sts_upt_result.scalar_one_or_none():
                        add_desc=EventsPendingCanceledStatus(
                            description=self.description,
                            event_id=self.event_id,
                            updated_at=current_time,
                            updated_date=current_date
                        )

                        self.session.add(add_desc)
                
                    await self.session.execute(
                        update(Events)
                        .where(Events.id==self.event_id)
                        .values(
                            status=self.event_status,
                            updated_by=user.name
                        )
                    )

                    await self.session.execute(
                        update(EventsAssignments)
                        .where(EventsAssignments.event_id==self.event_id)
                        .values(
                            is_completed=False
                        )
                    )
                    etag_to_del=[
                        f"events-{event.date}-etag",
                        WORKER_WITH_USER_ETAG_KEY
                    ]
                    await RedisCrud(key="").unlink_etag_from_redis(*etag_to_del)
                    ic(f"successfully event {self.event_status.value} status updated")
                    asyncio.create_task(
                        PushNotificationCrud(
                            notify_title=f"event status updated - {self.event_status.value}".title(),
                            notify_body=f"{event.name} on {current_date} at {current_time} updated-by {user.name}".title(),
                            data_payload={
                                "screen":"event_page"
                            }
                        ).push_notification_to_all()
                    )
                    return
                # raise HTTPException(
                #     status_code=404,
                #     detail=f"invalid event status {self.event_status.value}"
                # )
                ic(f"404 : invalid event status {self.event_status.value}")
                await send_error_notification(
                    user_id=self.user_id,
                    error_title="invalid event status".title(),
                    error_body=f"for {event.name} expected status 'pending or canceled' actual '{self.event_status.value}'".title,
                    notify_data_payload={
                        "screen":"home_screen"
                    }
                )


        except Exception as e:
            print(f"something went wrong while updating event {self.event_status.value} status {e}")
            await send_error_notification(
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
    def __init__(self,session:AsyncSession,image_id:str):
        self.session=session
        self.image_id=image_id
    async def get_image(self):
        try:
            image=(await self.session.execute(select(EventStatusImages).filter(EventStatusImages.id==self.image_id))).scalar_one_or_none()
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
            async with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                event=await EventVerification(session=self.session).is_event_exists_by_id(event_id=event_id)

                cont_desc_to_add_update=update(EventsContactDescription).where(EventsContactDescription.event_id==event_id).values(
                    description=contact_description,
                    updated_by=user.name,
                    updated_date=datetime.now().date(),
                    updated_at=await indian_time.get_india_time()
                ).returning(EventsContactDescription.id)

                cont_desc_to_add_update_result=await self.session.execute(cont_desc_to_add_update)

                if not cont_desc_to_add_update_result.scalar_one_or_none():
                    cont_desc=EventsContactDescription(
                        description=contact_description,
                        event_id=event_id,
                        updated_by=user.name,
                        updated_date=datetime.now().date(),
                        updated_at=await indian_time.get_india_time()
                    )

                    self.session.add(cont_desc)
                    await RedisCrud(key=f"events-{event.date}-etag").unlink_etag_from_redis()
                    return JSONResponse(
                        status_code=201,
                        content="call description added successfully"
                    )

                return JSONResponse(
                    status_code=200,
                    content="call description updated successfully"
                )
                
        except HTTPException:
            raise
        except Exception as e:
            ic(f"something went wrong while adding contact description {e}")
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while adding contact description {e}"
            )
        
    async def delete_description(self,contact_desc_id:int):
        try:
            async with self.session.begin():
                await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                cnt_desc_to_del=delete(EventsContactDescription).where(EventsContactDescription.id==contact_desc_id).returning(EventsContactDescription.event_id)
                cnt_desc_to_del_result=await self.session.execute(cnt_desc_to_del)
                event_id=cnt_desc_to_del_result.scalar_one_or_none()
                if event_id:
                    event_date=(await self.session.execute(select(Events.date).where(Events.id==event_id))).scalar_one_or_none()
                    await RedisCrud(key=f"events-{event_date}-etag").unlink_etag_from_redis()
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
            async with self.session.begin():
                await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                await EventVerification(session=self.session).is_event_exists_by_id(event_id=event_id)

                query_to_get=(await self.session.execute(
                    select(
                        EventsContactDescription.id,
                        EventsContactDescription.description,
                        EventsContactDescription.updated_by,
                        EventsContactDescription.updated_at,
                        EventsContactDescription.updated_date
                    ).where(
                        EventsContactDescription.event_id==event_id
                    )
                )).mappings().all()
                

                return query_to_get
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="something went wrong while deleting contact description {e}"
            )
                    

class EventAssignmentCrud:
    def __init__(self,session:AsyncSession,user_id:str):
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
            async def notify_assigned_workers(checked_workers:list):
                async with SessionLocal() as session:
                    for worker in checked_workers:
                        worker_user_id=worker['user_id']
                        if worker_user_id:
                            await NotificationsCrud(
                                session=session,
                                user_id=self.user_id,
                                is_for=worker_user_id
                            ).add_notification(
                                notify_title=notify_title,
                                notify_body=notify_body
                            )
                            order_dict=FirebaseCrud(user_id=worker_user_id).get_fcm_tokens()
                            ic(order_dict)
                            if order_dict:
                                asyncio.create_task(
                                    PushNotificationCrud(
                                        notify_title=notify_title,
                                        notify_body=notify_body,
                                        data_payload={
                                            "screen":"home_screen"
                                        }
                                    ).push_notifications_individually(fcm_tokens=order_dict)
                                    
                                )

                                ic("notified to assigned workers")
                                return      
            async with self.session.begin():
                
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
                    checked_workers=(await self.session.execute(select(Workers.id,Workers.user_id).where(Workers.name.in_(workers)))).mappings().all()
                    ic(checked_workers)
                    if len(workers)==len(checked_workers):
                        notify_title="Event Assignment".title()
                        notify_body=f"You are assigned to a event of {event.name} on {event.date} at {event.start_at}".title()

                        event_assign_to_update=update(EventsAssignments).where(EventsAssignments.event_id==event_id).values(
                            archagar=assigned_archagar,
                            abisegam=assigned_abisegam,
                            helper=assigned_helper,
                            poo=assigned_poo,
                            read=assigned_read,
                            prepare=assigned_prepare,
                            assigned_by=user.name,
                            assigned_datetime=cur_datetime_utc
                        ).returning(EventsAssignments.id)

                        result=await self.session.execute(event_assign_to_update)

                        if not result.scalar_one_or_none():
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

                        asyncio.create_task(notify_assigned_workers(checked_workers))
                        # redis etag deletee
                        await RedisCrud(key=f"events-{event.date}-etag").unlink_etag_from_redis()
                        # 
                        return f"Successfully workers assigned to {event.name}"
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
            async with self.session.begin():
                user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)

                if user.role==backend_enums.UserRole.ADMIN:
                    event_assig_to_del=delete(EventsAssignments).where(EventsAssignments.event_id==event_id).returning(EventsAssignments.event_id)
                    result = await self.session.execute(event_assig_to_del)
                    fetched_event_id=result.scalar_one_or_none()
                    if fetched_event_id:
                        # redis etag deletee
                        event_date=(await self.session.execute(select(Events.date).where(Events.id==fetched_event_id))).scalar_one_or_none()
                        await RedisCrud(key=f"events-{event_date}-etag").unlink_etag_from_redis()
                        # 
                        return "assigned event deleteed successfully"
                    raise HTTPException(
                        status_code=404,
                        detail="event id not found"
                    )
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
                worker_name=(await self.session.execute(select(Workers.name).where(Workers.user_id==user.id))).scalar_one_or_none()
            ic(worker_name)
            if worker_name:
                assigned_events=(await self.session.execute(
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
                )).mappings().all()

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