from sqlalchemy.orm import Session
from sqlalchemy import extract,select,func,cast, Date, Time,desc
from enums import backend_enums
from database.models.user import Users
from database.models.event import Events,Clients,Payments,EventsCompletedStatus,EventsPendingCanceledStatus,EventStatusImages,EventsNeivethiyam,NeivethiyamNames,EventsContactDescription,EventsAssignments
from database.operations.event_crud import EventNameAndAmountCrud,NeivethiyamNameAndAmountCrud
from database.operations.user_auth import UserVerification
from datetime import date
from fastapi.exceptions import HTTPException
from utils import document_generator,pdf_fields
from icecream import ic
import pandas as pd
from api.dependencies import email_automation
from pydantic import EmailStr
from typing import Optional


class __EventsCalendarInputs:
    def __init__(self,session:Session,user_id:str,month:int,year:int):
        self.session=session
        self.user_id=user_id
        self.month=month
        self.year=year

class __ParticularEventInputs:
    def __init__(self,session:Session,user_id:str,event_date:date,event_id:Optional[str]=None):
        self.session=session
        self.user_id=user_id
        self.event_date=event_date
        self.event_id=event_id

class __EventDropDownValuesInputs:
    def __init__(self,session:Session,user_id:str):
        self.session=session
        self.user_id=user_id

class __EventsToEmailInputs:
    def __init__(self,session:Session,user_id:str,from_date:date,to_date:date,file_type:backend_enums.FileType,to_email:EmailStr):
        self.session=session
        self.user_id=user_id
        self.from_date=from_date
        self.to_date=to_date
        self.file_type=file_type
        self.to_email=to_email

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
            condition=Events.date==self.event_date
            if self.event_id:
                condition=Events.id==self.event_id
                
            select_statement_columns=[
                Events.id.label("event_id"),
                Events.name.label("event_name"),
                Events.description.label("event_description"),
                Events.start_at.label("event_start_at"),
                Events.end_at.label("event_end_at"),
                Events.date.label('event_date'),
                Events.is_special.label('is_special_event'),
                Events.status.label("event_status"),
                Events.added_by.label("event_added_by"),
                Events.updated_by,
                Clients.name.label("client_name"),
                Clients.city.label("client_city"),
                Clients.mobile_number.label("client_mobile_number"),
                Payments.status.label("payment_status"),
                Payments.mode.label("payment_mode"),
                EventsCompletedStatus.feedback,
                EventsCompletedStatus.archagar,
                EventsCompletedStatus.abisegam,
                EventsCompletedStatus.helper,
                EventsCompletedStatus.poo,
                EventsCompletedStatus.read,
                EventsCompletedStatus.prepare,
                EventsCompletedStatus.image_url,
                EventsCompletedStatus.updated_date.label("completed_updated_date"),
                EventsCompletedStatus.updated_at.label("completed_updated_at"),
                EventsPendingCanceledStatus.description.label("event_pending_canceled_description"),
                EventsPendingCanceledStatus.updated_date.label("pending_canceled_updated_date"),
                EventsPendingCanceledStatus.updated_at.label("pending_canceled_updated_at"),
                EventsAssignments.abisegam.label('assigned_abisegam'),
                EventsAssignments.archagar.label('assigned_archagar'),
                EventsAssignments.helper.label("assigned_helper"),
                EventsAssignments.poo.label("assigned_poo"),
                EventsAssignments.read.label("assigned_read"),
                EventsAssignments.prepare.label("assigned_prepare"),
                EventsAssignments.assigned_by,
                EventsAssignments.assigned_datetime,
                NeivethiyamNames.id.label("neivethiyam_id"),
                NeivethiyamNames.name.label("neivethiyam_name"),
                EventsNeivethiyam.padi_kg,
                EventsContactDescription.id.label("contact_description_id"),
                EventsContactDescription.description.label("contact_description"),
                EventsContactDescription.updated_by.label("contact_description_updated_by"),
                EventsContactDescription.updated_at.label("contact_description_updated_at"),
                EventsContactDescription.updated_date.label("contact_description_updated_date")
            ]

            if user.role==backend_enums.UserRole.ADMIN:
                select_statement_columns.extend(
                    [
                        Payments.total_amount,
                        Payments.paid_amount,
                        NeivethiyamNames.amount.label("neivethiyam_amount"),
                    ]
                )

            events=self.session.execute(
                select(*select_statement_columns)
                .join(
                    Clients,Events.id==Clients.event_id,
                    isouter=True,
                )
                .join(
                    EventsNeivethiyam, Events.id == EventsNeivethiyam.event_id, 
                    isouter=True 
                )
                .join(
                    NeivethiyamNames,EventsNeivethiyam.neivethiyam_id==NeivethiyamNames.id,
                    isouter=True,
                )
                .join(
                    Payments,Events.id==Payments.event_id,
                    isouter=True,
                )
                .join(
                    EventsContactDescription,Events.id==EventsContactDescription.event_id,
                    isouter=True,
                )
                .join(
                    EventsCompletedStatus,Events.id==EventsCompletedStatus.event_id,
                    isouter=True
                )
                .join(
                    EventsPendingCanceledStatus,Events.id==EventsPendingCanceledStatus.event_id,
                    isouter=True,
                )
                .join(
                    EventsAssignments,EventsAssignments.event_id==Events.id,
                    isouter=True
                )
                .where(
                    condition
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
            neivethiyam_names=await NeivethiyamNameAndAmountCrud(session=self.session,user_id=self.user_id).get_neivethiyam_name_and_amount()
            return {"event_names":event_names['event_names'],"neivethiyam_names":neivethiyam_names["neivethiyam_names"],"payment_status":[i.value for i in backend_enums.PaymetStatus],"payment_modes":[i.value for i in backend_enums.PaymentMode]}
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while getting dropdown values {e}"
            )

class EventsToEmail(__EventsToEmailInputs):
    def get_events_email(self,user:Users):
        try:
            with self.session.begin():
                if user.role==backend_enums.UserRole.ADMIN:
                    select_statement_columns=[
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
                        Events.status.label("event_status"),
                        Events.added_by.label("event_added_by"),
                        Events.updated_by,
                        EventsCompletedStatus.feedback,
                        EventsCompletedStatus.archagar,
                        EventsCompletedStatus.abisegam,
                        EventsCompletedStatus.helper,
                        EventsCompletedStatus.poo,
                        EventsCompletedStatus.read,
                        EventsCompletedStatus.prepare,
                        EventsCompletedStatus.updated_date,
                        EventsCompletedStatus.updated_at,
                        Payments.total_amount,
                        Payments.paid_amount,
                        EventStatusImages.image,
                        NeivethiyamNames.name.label("neivethiyam_name"),
                        NeivethiyamNames.amount.label("neivethiyam_amount")
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
                            EventsNeivethiyam, Events.id == EventsNeivethiyam.event_id, 
                            isouter=True 
                        )
                        .join(
                            NeivethiyamNames,EventsNeivethiyam.neivethiyam_id==NeivethiyamNames.id,
                            isouter=True,
                        )
                        .join(
                            EventsCompletedStatus,Events.id==EventsCompletedStatus.event_id,
                            isouter=True,
                            
                        )
                        .join(
                            EventStatusImages,EventsCompletedStatus.id==EventStatusImages.event_sts_id,
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
                        file_name=f"{self.from_date}-{self.to_date}_eventReport.xlsx"
                        email_automation.send_events_report_as_excel(to_email=self.to_email,events=events,excel_filename=file_name,is_contains_image=True)
                    else:
                        file_name=f"{self.from_date}-{self.to_date}_eventReport.pdf"
                        ic(events[0]["event_name"])
                        for event in events:
                            pdf_byte=document_generator.generate_pdf(data=events,pdf_fields=pdf_fields.events_field_data(events=events),is_contain_image=True)
                        if pdf_byte:
                            email_automation.send_event_report_as_pdf(to_email=self.to_email,pdf_bytes=pdf_byte,pdf_filename=file_name)

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
