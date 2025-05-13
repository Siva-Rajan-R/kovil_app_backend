from sqlalchemy.orm import Session
from sqlalchemy import extract,select,func,case
from database.models.event import EventsStatus,Clients,Payments,Events
from database.operations.user_auth import UserVerification
from enums import backend_enums
from enums import backend_enums
from datetime import date
from fastapi.exceptions import HTTPException
from icecream import ic


class __EventDashboardInputs:
    def __init__(self,session:Session,user_id:str,from_date:date,to_date:date):
        self.session=session
        self.user_id=user_id
        self.from_date=from_date
        self.to_date=to_date

class EventDashboard(__EventDashboardInputs):
    async def get_dashboard(self):
        try:
            user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
            if user.role==backend_enums.UserRole.ADMIN:
                
                events_dashboard=self.session.execute(
                    select(
                        func.count(Events.id),
                        EventsStatus.status,
                        func.sum(Payments.total_amount).label("total_amount")
                    )
                    .join(EventsStatus,Events.id==EventsStatus.event_id,isouter=True)
                    .join(Payments,Events.id==Payments.event_id,isouter=True)
                    .where(
                        Events.date.between(self.from_date,self.to_date)
                    )
                    .group_by(
                        EventsStatus.status
                )
                ).mappings().all()



                # ic(today_completed,today_pending,today_cancled)
                return {
                    "events_dashboard":events_dashboard
                }
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



