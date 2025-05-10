from database.models.event import (
    Events,Clients,Payments,EventsStatus,EventNames,EventStatusImages,NeivethiyamNames,EventsNeivethiyam,EventsContactDescription
)
from database.models.workers import Workers
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
            neivethiyam_id:Optional[int]=None
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

class __EventAndNeivethiyamNameAndAmountCrudInputs:
    def __init__(self,session:Session,user_id:str):
        self.session=session
        self.user_id=user_id

class __DeleteEventInputs:
    def __init__(self,session:Session,user_id:str):
        self.session=session
        self.user_id=user_id

class __UpdateEventStatusInputs:
    def __init__(
            self,
            session:Session,
            user_id:str,
            event_id:str,
            event_status:backend_enums.EventStatus,
            feedback:str,
            archagar:str,
            abisegam:str,
            helper:str,
            poo:str,
            read:str,
            prepare:str,
            image:Optional[UploadFile],
            image_url_path:str,
            selected_workers_id:list[int]
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
        self.selected_workers_id=selected_workers_id
        self.image=image
        self.image_url_path=image_url_path

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
    async def add_event_name_and_amt(self,event_name:str,event_amount:int):
        try:
            with self.session.begin():
                user=await UserVerification(self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    added_event_name=EventNames(
                        name=event_name,
                        amount=event_amount
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
                        EventNames.amount
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
                    await EventNameVerification(session=self.session).is_event_name_exists_by_name(self.event_name)
                    event_id=await create_unique_id(self.event_name)
                    event=Events(
                        id=event_id,
                        name=self.event_name,
                        description=self.event_description,
                        date=self.event_date,
                        start_at=self.event_start_at,
                        end_at=self.event_end_at
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
                        
                    event_status=EventsStatus(
                        status=backend_enums.EventStatus.PENDING,
                        event_id=event_id,
                        added_by=user.name,
                        updated_at=await indian_time.get_india_time()
                    )

                    combined_event_details=[event,client,payment,event_status]

                    if self.neivethiyam_id:
                        await NeivethiyamNameVerification(session=self.session).is_neivethiyam_exists_by_id(self.neivethiyam_id)
                        event_neivethiyam=EventsNeivethiyam(
                            neivethiyam_id=self.neivethiyam_id,
                            event_id=event_id
                        )

                        combined_event_details.append(event_neivethiyam)

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

                    self.session.query(Events).filter(Events.id==event_id).update(
                        {
                            Events.name:self.event_name,
                            Events.description:self.event_description,
                            Events.date:self.event_date,
                            Events.start_at:self.event_start_at,
                            Events.end_at:self.event_end_at
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
                    if self.neivethiyam_id!=None:
                        await NeivethiyamNameVerification(session=self.session).is_neivethiyam_exists_by_id(self.neivethiyam_id)
                        query_to_update=self.session.query(EventsNeivethiyam).filter(EventsNeivethiyam.event_id==event_id)
                        if query_to_update.first():
                            query_to_update.update(
                                {
                                    EventsNeivethiyam.neivethiyam_id:self.neivethiyam_id
                                }
                            )
                        else:
                            self.session.add(
                                EventsNeivethiyam(
                                    neivethiyam_id=self.neivethiyam_id,
                                    event_id=event_id
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

class UpdateEventStatus(__UpdateEventStatusInputs):
    async def update_event_status(self):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
                await EventVerification(session=self.session).is_event_exists_by_id(self.event_id)

                
                update_dict={
                    EventsStatus.status:self.event_status,
                    EventsStatus.updated_by:user.name,
                    EventsStatus.feedback:self.feedback,
                    EventsStatus.archagar:self.archagar,
                    EventsStatus.abisegam:self.abisegam,
                    EventsStatus.helper:self.helper,
                    EventsStatus.poo:self.poo,
                    EventsStatus.read:self.read,
                    EventsStatus.prepare:self.prepare,
                    EventsStatus.updated_at:await indian_time.get_india_time(),
                    EventsStatus.updated_date:datetime.now().date()
                }
                event_status_query=self.session.query(EventsStatus).filter(EventsStatus.event_id==self.event_id)
                event_status=event_status_query.one_or_none()
                ic(self.image)
                ic(backend_enums.EventStatus.PENDING,backend_enums.EventStatus.PENDING.name,backend_enums.EventStatus.PENDING.value,self.event_status,event_status.image_url)

                for id in self.selected_workers_id:
                    query_to_update=self.session.query(Workers).filter(id==Workers.id)
                    if query_to_update.one_or_none():
                        query_to_update.update(
                            {
                                Workers.no_of_participated_events:query_to_update.one_or_none().no_of_participated_events+1
                            }
                        )
                    else:
                        raise HTTPException(
                            status_code=404,
                            detail="Invalid worker names"
                        )
                    
                if self.image and not event_status.image_url:
                    image_id=await create_unique_id(self.feedback)
                    ei_to_add=EventStatusImages(
                        id=image_id,
                        image=self.image.file.read(),
                        event_sts_id=event_status.id
                    )
                    self.session.add(ei_to_add)
                    update_dict[EventsStatus.image_url]=self.image_url_path+image_id
                    
                elif self.event_status==backend_enums.EventStatus.CANCELED or self.event_status==backend_enums.EventStatus.PENDING:
                    print("hello from ")
                    self.session.query(EventStatusImages).filter(EventStatusImages.event_sts_id==event_status.id).delete()
                    update_dict[EventsStatus.image_url]=None

                elif self.image and event_status.image_url:
                    self.session.query(EventStatusImages).filter(EventStatusImages.event_sts_id==event_status.id).update(
                        {
                            EventStatusImages.image:self.image.file.read()
                        }
                    )

                event_status_query.update(
                    update_dict
                )

                return "event status updated successfully"
            
        except HTTPException:
            raise

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while updating event status {e}"
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
                    