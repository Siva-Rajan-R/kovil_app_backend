from database.models.event import Events,Clients,Payments,EventsStatus
from sqlalchemy.orm import Session
from sqlalchemy import select
from enums import backend_enums
from security.uuid_creation import create_unique_id
from datetime import date,time
from pydantic import EmailStr
from fastapi.exceptions import HTTPException
from database.operations.user_auth import UserVerification
from typing import Optional

class __AddEventInputs:
    def __init__(
            self,
            session:Session,
            user_id:str,
            event_name:str,
            event_description:str,
            event_date:date,
            event_start_at:time,
            event_end_at:time,
            client_name:str,
            client_mobile_number:str,
            client_email:Optional[EmailStr],
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
        self.client_email=client_email
        self.total_amount=total_amount
        self.paid_amount=paid_amount
        self.payment_status=payment_status
        self.payment_mode=payment_mode

class __DeleteEventInputs:
    def __init__(self,session:Session,user_id:str,event_id:str):
        self.session=session
        self.user_id=user_id
        self.event_id=event_id

class __UpdateEventStatusInputs:
    def __init__(self,session:Session,user_id:str,event_id:str,event_status:backend_enums.EventStatus):
        self.session=session
        self.user_id=user_id
        self.event_id=event_id
        self.event_status=event_status

class EventVerification:
    def __init__(self,session:Session):
        self.session=session

    async def is_event_exists_by_id(self,event_id:str):
        if self.session.execute(select(Events.id).where(Events.id==event_id)).scalar_one_or_none():
            return True
        raise HTTPException(
            status_code=404,
            detail="event not found"
        )
    
class AddEvent(__AddEventInputs):
    async def add_event(self):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
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
                        email=self.client_email,
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
                        added_by=self.user_id
                    )

                    combined_event_details=[event,client,payment,event_status]
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
                await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
                await EventVerification(session=self.session).is_event_exists_by_id(self.event_id)
                self.session.query(EventsStatus).filter(EventsStatus.event_id==self.event_id).update(
                    {
                        EventsStatus.status:self.event_status,
                        EventsStatus.updated_by:self.user_id
                    }
                )

                return "event status updated successfully"
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while updating event status {e}"
            )
