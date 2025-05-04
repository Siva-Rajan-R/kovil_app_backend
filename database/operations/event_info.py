from sqlalchemy.orm import Session
from sqlalchemy import extract,select,func,cast, Date, Time,desc
from enums import backend_enums
from database.models.event import Events,Clients,Payments,EventsStatus,EventStatusImages
from database.operations.event_crud import EventNameAndAmountCrud
from database.operations.user_auth import UserVerification
from datetime import date
from fastapi.exceptions import HTTPException
from utils.document_generator import generate_pdf
from icecream import ic
import pandas as pd
from api.dependencies import email_automation


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

class __EventDropDownValuesInputs:
    def __init__(self,session:Session,user_id:str):
        self.session=session
        self.user_id=user_id

class __EventsToEmailInputs:
    def __init__(self,session:Session,user_id:str,from_date:date,to_date:date,file_type:backend_enums.FileType):
        self.session=session
        self.user_id=user_id
        self.from_date=from_date
        self.to_date=to_date
        self.file_type=file_type

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

            if user.role==backend_enums.UserRole.ADMIN:
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
                    
                    
                )
                .join(
                    Payments,Events.id==Payments.event_id,
                    isouter=True,
                    
                    
                )
                .join(
                    EventsStatus,Events.id==EventsStatus.event_id,
                    isouter=True,
                    
                )
                .where(
                    Events.date==self.event_date
                )
                .order_by(
                    cast(Events.date, Date),
                    cast(Events.start_at, Time)
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
        
class EventDropDownValues(__EventDropDownValuesInputs):
    async def get_dropdown_values(self):
        try:
            event_names=await EventNameAndAmountCrud(session=self.session,user_id=self.user_id).get_event_name_and_amount()

            return {"event_names":event_names['event_names'],"payment_status":[i.value for i in backend_enums.PaymetStatus],"payment_modes":[i.value for i in backend_enums.PaymentMode]}
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while getting dropdown values {e}"
            )

class EventsToEmail(__EventsToEmailInputs):
    async def get_event_emails(self):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
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
                        EventsStatus.updated_date,
                        EventsStatus.updated_at,
                        Payments.total_amount,
                        Payments.paid_amount,
                        EventStatusImages.image
                    ]

                    events=self.session.execute(
                        select(*select_statement_columns)
                        .join(
                            Clients,Events.id==Clients.event_id,
                            isouter=True,
                        )
                        .join(
                            Payments,Events.id==Payments.event_id,
                            isouter=True,
                            
                            
                        )
                        .join(
                            EventsStatus,Events.id==EventsStatus.event_id,
                            isouter=True,
                            
                        )
                        .join(
                            EventStatusImages,EventsStatus.id==EventStatusImages.event_sts_id,
                            isouter=True
                        )
                        .where(
                            Events.date>=self.from_date,
                            Events.date<=self.to_date
                        )
                        .order_by(
                            cast(Events.date, Date),
                            cast(Events.start_at, Time)
                        )
                    ).mappings().all()
                
                    if self.file_type==backend_enums.FileType.EXCEL:
                        df = pd.DataFrame(events)
                        file_name=f"{self.from_date}-{self.to_date}_eventReport.xlsx"
                        df.to_excel(file_name, index=False)

                        await email_automation.send_events_report_as_excel("siva967763@gmail.com",events=events,excel_file=file_name)
                    else:
                        file_name=f"{self.from_date}-{self.to_date}_eventReport.pdf"
                        if await generate_pdf(events,output_file=file_name):
                            await email_automation.send_event_report_as_pdf("siva967763@gmail.com",pdf_file=file_name)

                    return "successfully sended"
                raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to get this information"
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while geting events for email : {e}"
            )