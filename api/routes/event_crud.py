from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from database.operations.event_crud import AddEvent,DeleteEvent,UpdateEventStatus,Session
from database.main import get_db_session
from api.dependencies.token_verification import verify
from api.schemas.event_crud import AddEventSchema,DeleteEventSchema,UpdateEventStatusSchema

router=APIRouter(
    tags=["Add,Update and Delete Events"]
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
        client_email=add_event_inputs.client_email,
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
async def update_event_status(update_event_status_inputs:UpdateEventStatusSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user["id"]
    event_status=await UpdateEventStatus(
        session=session,
        user_id=user_id,
        event_id=update_event_status_inputs.event_id,
        event_status=update_event_status_inputs.event_status
    ).update_event_status()

    return JSONResponse(
        status_code=200,
        content=event_status
    )


