from sqlalchemy.orm import Session
from sqlalchemy import extract,select,func,case
from database.models.event import EventsStatus,Clients,Payments,Events
from database.operations.user_auth import UserVerification,UserRole
from enums import backend_enums
from datetime import date
from fastapi.exceptions import HTTPException
from icecream import ic


class __EventDashboardInputs:
    def __init__(self,session:Session,user_id:str,date:date):
        self.session=session
        self.user_id=user_id
        self.date=date

class EventDashboard(__EventDashboardInputs):
    async def get_dashboard(self):
        try:
            user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
            if user.role==UserRole.ADMIN:
                
                today_completed=self.session.execute(
                    select(
                        func.count(Payments.event_id),
                        func.sum(Payments.paid_amount)
                    )
                    .where(
                        EventsStatus.status==backend_enums.EventStatus.COMPLETED,
                        Events.date==self.date
                    )
                ).mappings().all()

                today_cancled=self.session.execute(
                    select(
                        func.count(Payments.event_id),
                        func.sum(Payments.paid_amount)
                    )
                    .where(
                        EventsStatus.status==backend_enums.EventStatus.CANCLED,
                        Events.date==self.date
                    )
                ).mappings().all()

                today_pending=self.session.execute(
                    select(
                        func.count(Events.date),
                        func.sum(Payments.paid_amount)
                    )
                    .where(
                        EventsStatus.status==backend_enums.EventStatus.PENDING,
                        Events.date==self.date
                    )
                ).mappings().all()


                ic(today_completed,today_pending,today_cancled)
                return
            raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to make any changes"
                )
                
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while fetching dashboard {e}"
            )



