from fastapi import APIRouter,Depends,Request,UploadFile,File,Form,Response,HTTPException
from enums import backend_enums
from fastapi.responses import JSONResponse
from database.operations.event_crud import AddEvent,DeleteEvent,UpdateEventStatus,Session,AddEventName,GetEventStatusImage
from database.main import get_db_session
from api.dependencies.token_verification import verify
from api.schemas.event_crud import AddEventSchema,DeleteEventSchema,AddEventNameSchema,DeleteEventNameSchema
from typing import Optional

router=APIRouter(
    tags=["Add,Update and Delete Events and EventName"]
)


@router.post("/event/name")
async def add_event_name(event_name_inp:AddEventNameSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    added_event_name=await AddEventName(
        session=session,
        user_id=user_id
    ).add_event_name(event_name=event_name_inp.event_name,event_amount=event_name_inp.event_amount)

    return JSONResponse(
        status_code=201,
        content=added_event_name
    )

@router.delete("/event/name")
async def add_event_name(en_del_inp:DeleteEventNameSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    added_event_name=await AddEventName(
        session=session,
        user_id=user_id
    ).delete_event_name(event_name_id=en_del_inp.event_name_id)

    return JSONResponse(
        status_code=201,
        content=added_event_name
    )

@router.post("/event")
async def add_event(add_event_inputs:AddEventSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user["id"]
    added_event=await AddEvent(
        user_id=user_id,
        session=session,
        event_name=add_event_inputs.event_name,
        event_description=add_event_inputs.event_description,
        event_date=add_event_inputs.event_date,
        event_start_at=add_event_inputs.event_start_at,
        event_end_at=add_event_inputs.event_end_at,
        client_name=add_event_inputs.client_name,
        client_mobile_number=add_event_inputs.client_mobile_number,
        client_city=add_event_inputs.client_city,
        total_amount=add_event_inputs.total_amount,
        paid_amount=add_event_inputs.paid_amount,
        payment_status=add_event_inputs.payment_status,
        payment_mode=add_event_inputs.payment_mode,
    ).add_event()

    return JSONResponse(
        status_code=201,
        content=added_event
    )

@router.delete("/event")
async def delete_event(delete_event_inputs:DeleteEventSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user["id"]
    deleted_event=await DeleteEvent(
        session=session,
        user_id=user_id,
        event_id=delete_event_inputs.event_id
    ).delete_event()

    return JSONResponse(
        status_code=200,
        content=deleted_event
    )

@router.put("/event/status")
async def update_event_status(
    request:Request,
    session:Session=Depends(get_db_session),
    user:dict=Depends(verify),
    event_id:str=Form(...),
    event_status:backend_enums.EventStatus=Form(backend_enums.EventStatus.PENDING),
    feedback:str=Form(...),
    tips:str=Form(...),
    poojai:str=Form(...),
    abisegam:str=Form(...),
    helper:str=Form(...),
    poo:str=Form(...),
    read:str=Form(...),
    prepare:str=Form(...),
    tips_shared:str=Form(...),
    tips_given_to:str=Form(...),
    image:Optional[UploadFile]=File(None)
):
    fields = [event_id, feedback, tips, poojai, abisegam, helper, poo, read, prepare, tips_shared, tips_given_to]
    
    if any(not field.strip() for field in fields) and event_status!="":
        raise HTTPException(
            status_code=422,
            detail="input fields could not be empty"
        )
    user_id=user["id"]
    event_status=await UpdateEventStatus(
        session=session,
        user_id=user_id,
        event_id=event_id,
        event_status=event_status,
        feedback=feedback,
        tips=tips,
        poojai=poojai,
        abisegam=abisegam,
        helper=helper,
        poo=poo,
        read=read,
        prepare=prepare,
        tips_shared=tips_shared,
        tips_given_to=tips_given_to,
        image_url_path=str(request.base_url)+"event/status/image/",
        image=image
    ).update_event_status()

    return JSONResponse(
        status_code=200,
        content=event_status
    )

@router.get("/event/status/image/{image_id}")
async def get_event_status_image(image_id:str,session:Session=Depends(get_db_session)):
    image=await GetEventStatusImage(
        session=session,
        image_id=image_id
    ).get_image()

    return Response(
        content=image,
        status_code=200,
        media_type='image/jpg'
    )