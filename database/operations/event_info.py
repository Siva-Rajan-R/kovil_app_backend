from sqlalchemy.orm import Session
from sqlalchemy import extract,select,func
from database.models.event import Events,Clients,Payments,EventsStatus
from database.operations.user_auth import UserVerification,UserRole
from datetime import date
from fastapi.exceptions import HTTPException
from icecream import ic


class __EventsCalendarInputs:
    def __init__(self,session:Session,user_id:str,month:int,year:int):
        self.session=session
        self.user_id=user_id
        self.month=month
        self.year=year

class __ParticularEventInputs:
    def __init__(self,session:Session,user_id:str,event_date:date):
        self.session=session
        self.user_id=user_id
        self.event_date=event_date

class EventCalendar(__EventsCalendarInputs):
    async def get_event_calendar(self):
        try:
            await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
            events=self.session.execute(
                select(
                    Events.date
                )
                .where(
                    extract("month",Events.date)==self.month,
                    extract("year",Events.date)==self.year
                )
            ).scalars().all()

            ic({"events":events})
            return {"events":events}
        
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while fetching event calendar {e}"
            )
        
class ParticularEvent(__ParticularEventInputs):
    async def get_events(self):
        try:
            user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
            select_statement_columns=[
                Events.id.label("event_id"),
                Events.name.label("event_name"),
                Events.description.label("event_description"),
                Events.start_at.label("event_start_at"),
                Events.end_at.label("event_end_at"),
                Events.date.label('event_date'),
                Clients.name.label("client_name"),
                Clients.city.label("client_city"),
                Clients.mobile_number.label("client_mobile_number"),
                Payments.status.label("payment_status"),
                Payments.mode.label("payment_mode"),
                EventsStatus.status.label("event_status"),
                EventsStatus.added_by.label("event_added_by"),
                EventsStatus.updated_by,
                EventsStatus.feedback,
                EventsStatus.tips,
                EventsStatus.poojai,
                EventsStatus.abisegam,
                EventsStatus.helper,
                EventsStatus.poo,
                EventsStatus.read,
                EventsStatus.prepare,
                EventsStatus.tips_shared,
                EventsStatus.tips_given_to,
                EventsStatus.image_url,
                EventsStatus.updated_date,
                EventsStatus.updated_at

            ]

            if user.role==UserRole.ADMIN:
                select_statement_columns.extend(
                    [
                        Payments.total_amount,
                        Payments.paid_amount
                    ]
                )

            events=self.session.execute(
                select(*select_statement_columns)
                .join(
                    Clients,Events.id==Clients.event_id,
                    isouter=True,
                    full=True
                    
                )
                .join(
                    Payments,Events.id==Payments.event_id,
                    isouter=True,
                    full=True
                    
                )
                .join(
                    EventsStatus,Events.id==EventsStatus.event_id,
                    isouter=True,
                    full=True
                )
                .where(
                    Events.date==self.event_date
                )
            ).mappings().all()

            ic({"events":events})

            return {"events":events}
        
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while fetching particular event {e}"
            )