from database.models.event import Events,Clients,Payments,EventsStatus,EventNames,EventStatusImages
from fastapi import UploadFile
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
            payment_mode:backend_enums.PaymentMode
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

class __EventNameAndAmountCrudInputs:
    def __init__(self,session:Session,user_id:str):
        self.session=session
        self.user_id=user_id

class __DeleteEventInputs:
    def __init__(self,session:Session,user_id:str,event_id:str):
        self.session=session
        self.user_id=user_id
        self.event_id=event_id

class __UpdateEventStatusInputs:
    def __init__(
            self,
            session:Session,
            user_id:str,
            event_id:str,
            event_status:backend_enums.EventStatus,
            feedback:str,
            tips:str,
            poojai:str,
            abisegam:str,
            helper:str,
            poo:str,
            read:str,
            prepare:str,
            tips_shared:str,
            tips_given_to:str,
            image:Optional[UploadFile],
            image_url_path:str
        ):
        self.session=session
        self.user_id=user_id
        self.event_id=event_id
        self.event_status=event_status
        self.feedback=feedback
        self.tips=tips
        self.poojai=poojai
        self.abisegam=abisegam
        self.helper=helper
        self.poo=poo
        self.read=read
        self.prepare=prepare
        self.tips_shared=tips_shared
        self.tips_given_to=tips_given_to
        self.image=image
        self.image_url_path=image_url_path

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

class EventNameAndAmountCrud(__EventNameAndAmountCrudInputs):
    async def add_event_name_and_amt(self,event_name:str,event_amount:str):
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
                    self.session.delete(en_to_delete)

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
                    
class AddEvent(__AddEventInputs):
    async def add_event(self):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    if self.session.query(EventNames).filter(EventNames.name==self.event_name).first():
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
                        self.session.add_all(combined_event_details)

                        return "successfully event added"
                    raise HTTPException(
                        status_code=404,
                        detail=f"There is no event name as {self.event_name}"
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
                detail=f"something went wrong while adding event details {e}"
            )

class UpdateEvent(__AddEventInputs):
    async def update_event(self,event_id:str):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                if user==backend_enums.UserRole.ADMIN:
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
    async def delete_event(self):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                await EventVerification(session=self.session).is_event_exists_by_id(self.event_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    event=self.session.query(Events).filter(Events.id==self.event_id).first()
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
                    EventsStatus.tips:self.tips,
                    EventsStatus.poojai:self.poojai,
                    EventsStatus.abisegam:self.abisegam,
                    EventsStatus.helper:self.helper,
                    EventsStatus.poo:self.poo,
                    EventsStatus.read:self.read,
                    EventsStatus.prepare:self.prepare,
                    EventsStatus.tips_shared:self.tips_shared,
                    EventsStatus.tips_given_to:self.tips_given_to,
                    EventsStatus.updated_at:await indian_time.get_india_time(),
                    EventsStatus.updated_date:datetime.now().date()
                }
                event_status_query=self.session.query(EventsStatus).filter(EventsStatus.event_id==self.event_id)
                event_status=event_status_query.one_or_none()
                ic(self.image)
                ic(backend_enums.EventStatus.PENDING,backend_enums.EventStatus.PENDING.name,backend_enums.EventStatus.PENDING.value,self.event_status,event_status.image_url)
                if self.image and not event_status.image_url:
                    image_id=await create_unique_id(self.feedback)
                    ei_to_add=EventStatusImages(
                        id=image_id,
                        image=self.image.file.read(),
                        event_sts_id=self.session.query(func.max(EventsStatus.id)).scalar()
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
