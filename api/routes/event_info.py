from fastapi import APIRouter,Depends,Query,Request,Response,HTTPException
from security.entity_tag import generate_entity_tag
from database.operations.event_info import EventCalendar,ParticularEvent,AsyncSession,date,EventDropDownValues
from database.main import get_db_session
from api.dependencies.token_verification import verify
from typing import Optional
from redis_db.redis_crud import RedisCrud
from redis_db.redis_etag_keys import DROP_DOWN_ETAG_KEY,BOOKED_EVENTS
from icecream import ic


router=APIRouter(
    tags=["Get Event Informations"],
    prefix="/event"
)

@router.get("/calendar")
async def event_calendar(response:Response,request:Request,month:int=Query(...),year:int=Query(...),user:dict=Depends(verify),session:AsyncSession=Depends(get_db_session)):
    redis_crud=RedisCrud(key=f"event-calendar-{month}-{year}-etag")
    redis_etag=await redis_crud.get_etag_from_redis()
    ic(redis_etag)
    if redis_etag:
        if request.headers.get('if-none-match')==redis_etag:
            raise HTTPException(
                status_code=304
            )
    ec=await EventCalendar(
        session=session,
        user_id=user["id"],
        month=month,
        year=year
    ).get_event_calendar()
    etag=generate_entity_tag(str(ec))
    response.headers['ETag']=etag
    await redis_crud.store_etag_to_redis(etag=etag)
    return ec

@router.get("/specific",response_model_exclude_none=True)
async def event_specific(request:Request,response:Response,date:date=Query(...),event_id:Optional[str]=Query(None),isfor_booked:Optional[bool]=Query(None),user:dict=Depends(verify),session:AsyncSession=Depends(get_db_session)):
    
    redis_crud=RedisCrud(key=f"events-{date}-etag")
    if isfor_booked:
        ic(isfor_booked)
        redis_crud=RedisCrud(key=BOOKED_EVENTS)
    redis_etag=await redis_crud.get_etag_from_redis()
    if redis_etag:
        if request.headers.get('if-none-match')==redis_etag:
            raise HTTPException(
                status_code=304
            )
        
    events=await ParticularEvent(
        session=session,
        user_id=user['id'],
        event_date=date,
        event_id=event_id,
        isfor_booked=isfor_booked
    ).get_events()
    etag=generate_entity_tag(str(events))
    response.headers['ETag']=etag
    await redis_crud.store_etag_to_redis(etag=etag)
    return events

@router.get("/dropdown-values")
async def get_event_dropdown_values(request:Request,response:Response,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    redis_crud=RedisCrud(key=DROP_DOWN_ETAG_KEY)
    redis_etag=await redis_crud.get_etag_from_redis()
    ic(redis_etag)
    if redis_etag:
        if request.headers.get("if-none-match")==redis_etag:
            raise HTTPException(
                status_code=304,
            )
    event_dd_values=await EventDropDownValues(session=session,user_id=user_id).get_dropdown_values()
    etag=generate_entity_tag(data=str(event_dd_values))
    response.headers['X-Custom-Cache']=etag
    await redis_crud.store_etag_to_redis(etag=etag)
    return event_dd_values

