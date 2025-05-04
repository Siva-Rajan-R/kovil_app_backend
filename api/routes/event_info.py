from fastapi import APIRouter,Depends,Query
from database.operations.event_info import EventCalendar,ParticularEvent,Session,date,EventDropDownValues,EventsToEmail
from database.main import get_db_session
from api.dependencies.token_verification import verify
from enums import backend_enums

router=APIRouter(
    tags=["Get Event Informations"]
)

@router.get("/event/calendar")
async def event_calendar(month:int=Query(...),year:int=Query(...),user:dict=Depends(verify),session:Session=Depends(get_db_session)):
    ec=await EventCalendar(
        session=session,
        user_id=user["id"],
        month=month,
        year=year
    ).get_event_calendar()

    return ec

@router.get("/event/specific")
async def event_specific(date:date=Query(...),user:dict=Depends(verify),session:Session=Depends(get_db_session)):
    events=await ParticularEvent(
        session=session,
        user_id=user['id'],
        event_date=date
    ).get_events()

    return events

@router.get("/event/dropdown-values")
async def get_event_dropdown_values(session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    event_dd_values=await EventDropDownValues(session=session,user_id=user_id).get_dropdown_values()
    return event_dd_values

@router.get("/event/report/email")
async def get_event_emails(file_type:backend_enums.FileType=Query(...),from_date:date=Query(...),to_date:date=Query(...),session:Session=Depends(get_db_session)):
    events=await EventsToEmail(
        session=session,
        user_id="f5903517-ea0f-5451-8c52-61b7da430d32",
        from_date=from_date,
        to_date=to_date,
        file_type=file_type
    ).get_event_emails()

    return events