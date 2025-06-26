from fastapi import APIRouter,Depends,Query,Request,Response,HTTPException
from security.entity_tag import generate_entity_tag
from database.operations.event_info import EventCalendar,ParticularEvent,Session,date,EventDropDownValues
from database.main import get_db_session
from api.dependencies.token_verification import verify
from typing import Optional


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

@router.get("/event/specific",response_model_exclude_none=True)
async def event_specific(date:date=Query(...),event_id:Optional[str]=Query(None),user:dict=Depends(verify),session:Session=Depends(get_db_session)):
    events=await ParticularEvent(
        session=session,
        user_id=user['id'],
        event_date=date,
        event_id=event_id
    ).get_events()

    return events

@router.get("/event/dropdown-values")
async def get_event_dropdown_values(request:Request,response:Response,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    event_dd_values=await EventDropDownValues(session=session,user_id=user_id).get_dropdown_values()
    etag=generate_entity_tag(data=str(event_dd_values))

    if request.headers.get("if-none-match")==etag:
        raise HTTPException(
            status_code=304,
        )
    
    response.headers['ETag']=etag
    return event_dd_values

