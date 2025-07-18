from fastapi import APIRouter,Depends,Request,UploadFile,File,Form,Response,HTTPException,BackgroundTasks,Query
from enums import backend_enums
from fastapi.responses import ORJSONResponse,StreamingResponse
from database.operations.event_crud import AddEvent,DeleteEvent,UpdateEvent,UpdateEventCompletedStatus,UpdateEventPendingCanceledStatus,AsyncSession,EventNameAndAmountCrud,GetEventStatusImage,NeivethiyamNameAndAmountCrud,ContactDescription,EventAssignmentCrud
from database.operations.event_info import EventsToEmail
from database.main import get_db_session
from api.dependencies.token_verification import verify
from api.schemas.event_crud import AddEventSchema,UpdateEventSchema,UpdateEventPendingCanceledStatusSchema,DeleteAllEventSchema,DeleteSingleEventSchema,AddEventNameSchema,DeleteEventNameSchema,GetEventsEmailschema,AddNeivethiyamNameSchema,DeleteNeivethiyamNameSchema,AddContactDescriptionSchema,DeleteContactDescriptionSchema,AddEventAssignmentSchema,DeleteEventAssignmentSchema
from typing import Optional,List
from database.operations.user_auth import UserVerification
from security.entity_tag import generate_entity_tag
from utils.clean_ph_numbers import clean_phone_numbers
from utils.image_compression import compress_image_to_target_size
from utils.async_to_sync_bgtask import run_async_in_bg
from icecream import ic
from io import BytesIO
import asyncio
from redis_db.redis_crud import RedisCrud
from redis_db.redis_etag_keys import EVENT_NAME_ETAG_KEY,NEIVETHIYAM_ETAG_KEY
from typing import Literal

router=APIRouter(
    tags=["Add,Update and Delete Events and EventName"]
)



@router.get("/event/name")
async def get_event_name_and_amount(request:Request,response:Response,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']

    redis_crud=RedisCrud(key=EVENT_NAME_ETAG_KEY)

    redis_etag=await redis_crud.get_etag_from_redis()
    ic(redis_etag)
    if redis_etag:
        if request.headers.get("if-none-match")==redis_etag:
            raise HTTPException(
                status_code=304,
            )
        
    event_names=await EventNameAndAmountCrud(
        session=session,
        user_id=user_id
    ).get_event_name_and_amount()

    etag=generate_entity_tag(data=str(event_names))

    await redis_crud.store_etag_to_redis(etag=etag)
    response.headers['ETag']=etag

    return event_names

@router.post("/event/name")
async def add_event_name_and_amount(event_name_inp:AddEventNameSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    added_event_name=await EventNameAndAmountCrud(
        session=session,
        user_id=user_id
    ).add_event_name_and_amt(event_name=event_name_inp.event_name,event_amount=event_name_inp.event_amount,is_special=event_name_inp.is_special)
    
    await RedisCrud(key=EVENT_NAME_ETAG_KEY).unlink_etag_from_redis()
    return ORJSONResponse(
        status_code=201,
        content=added_event_name
    )

@router.delete("/event/name")
async def delete_event_name_and_amount(en_del_inp:DeleteEventNameSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    delete_event_name=await EventNameAndAmountCrud(
        session=session,
        user_id=user_id
    ).delete_event_name_and_amount(event_name=en_del_inp.event_name)

    await RedisCrud(key=EVENT_NAME_ETAG_KEY).unlink_etag_from_redis()
    return ORJSONResponse(
        status_code=200,
        content=delete_event_name
    )

#neivethiyam
@router.get("/neivethiyam/name")
async def get_neivethiyam_name_and_amount(request:Request,response:Response,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    
    redis_crud=RedisCrud(key=NEIVETHIYAM_ETAG_KEY)
    
    redis_etag=await redis_crud.get_etag_from_redis()
    ic(redis_etag)
    if redis_etag:
        if request.headers.get("if-none-match")==redis_etag:
            raise HTTPException(
                status_code=304,
            )
    
    neivethiyam_names=await NeivethiyamNameAndAmountCrud(
        session=session,
        user_id=user_id
    ).get_neivethiyam_name_and_amount()

    etag=generate_entity_tag(data=str(neivethiyam_names))
    await redis_crud.store_etag_to_redis(etag=etag)
    response.headers['ETag']=etag

    return neivethiyam_names

@router.post("/neivethiyam/name")
async def add_neivethiyam_name_and_amount(neivethiyam_name_inp:AddNeivethiyamNameSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    added_neivethiyam_name=await NeivethiyamNameAndAmountCrud(
        session=session,
        user_id=user_id
    ).add_neivethiyam_name_and_amt(neivethiyam_name=neivethiyam_name_inp.neivethiyam_name,neivethiyam_amount=neivethiyam_name_inp.neivethiyam_amount)

    await RedisCrud(key=NEIVETHIYAM_ETAG_KEY).unlink_etag_from_redis()
    return ORJSONResponse(
        status_code=201,
        content=added_neivethiyam_name
    )

@router.delete("/neivethiyam/name")
async def delete_neivethiyam_name_and_amount(en_del_inp:DeleteNeivethiyamNameSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    deleted_neivethiyam_name=await NeivethiyamNameAndAmountCrud(
        session=session,
        user_id=user_id
    ).delete_neivethiyam_name_and_amount(neivethiyam_name=en_del_inp.neivethiyam_name)
    await RedisCrud(key=NEIVETHIYAM_ETAG_KEY).unlink_etag_from_redis()
    return ORJSONResponse(
        status_code=200,
        content=deleted_neivethiyam_name
    )

@router.post("/event")
async def add_event(bgt:BackgroundTasks,add_event_inputs:AddEventSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user["id"]
    print(add_event_inputs.neivethiyam_id)
    if len(add_event_inputs.client_mobile_number)>10:
        add_event_inputs.client_mobile_number=await clean_phone_numbers(add_event_inputs.client_mobile_number)
    print(add_event_inputs.client_mobile_number)
    added_event=await AddEvent(
        user_id=user_id,
        session=session,
        bg_task=bgt,
        event_name=add_event_inputs.event_name,
        event_description=add_event_inputs.event_description,
        event_date=add_event_inputs.event_date,
        event_start_at=add_event_inputs.event_start_at,
        event_end_at=add_event_inputs.event_end_at,
        client_name=add_event_inputs.client_name,
        client_mobile_number=add_event_inputs.client_mobile_number,
        client_city=add_event_inputs.client_city,
        client_email=add_event_inputs.client_email,
        total_amount=add_event_inputs.total_amount,
        paid_amount=add_event_inputs.paid_amount,
        payment_status=add_event_inputs.payment_status,
        payment_mode=add_event_inputs.payment_mode,
        neivethiyam_id=add_event_inputs.neivethiyam_id,
        is_special=add_event_inputs.is_special,
        padi_kg=add_event_inputs.neivethiyam_kg
    ).add_event()


    return ORJSONResponse(
        status_code=201,
        content=added_event
    )

@router.put("/event")
async def update_event(bgt:BackgroundTasks,update_event_inputs:UpdateEventSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user["id"]
    if len(update_event_inputs.client_mobile_number)>10:
        update_event_inputs.client_mobile_number=await clean_phone_numbers(update_event_inputs.client_mobile_number)
        
    updated_event=await UpdateEvent(
        bg_task=bgt,
        user_id=user_id,
        session=session,
        event_name=update_event_inputs.event_name,
        event_description=update_event_inputs.event_description,
        event_date=update_event_inputs.event_date,
        event_start_at=update_event_inputs.event_start_at,
        event_end_at=update_event_inputs.event_end_at,
        client_name=update_event_inputs.client_name,
        client_mobile_number=update_event_inputs.client_mobile_number,
        client_city=update_event_inputs.client_city,
        client_email=update_event_inputs.client_email,
        total_amount=update_event_inputs.total_amount,
        paid_amount=update_event_inputs.paid_amount,
        payment_status=update_event_inputs.payment_status,
        payment_mode=update_event_inputs.payment_mode,
        neivethiyam_id=update_event_inputs.neivethiyam_id,
        is_special=update_event_inputs.is_special,
        padi_kg=update_event_inputs.neivethiyam_kg
    ).update_event(event_id=update_event_inputs.event_id)

    return ORJSONResponse(
        status_code=200,
        content=updated_event
    )

@router.delete("/event")
async def delete_single_event(delete_event_inputs:DeleteSingleEventSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user["id"]
    deleted_event=await DeleteEvent(
        session=session,
        user_id=user_id
    ).delete_single_event(event_id=delete_event_inputs.event_id)

    return ORJSONResponse(
        status_code=200,
        content=deleted_event
    )

@router.delete("/event/all")
async def delete_all_event(request:Request,bgt:BackgroundTasks,delete_event_inputs:DeleteAllEventSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user["id"]
    asyncio.create_task(
        DeleteEvent(
            session=session,
            user_id=user_id
        ).delete_all_event(
            from_date=delete_event_inputs.from_date,
            to_date=delete_event_inputs.to_date
        )
    )

    return f"{delete_event_inputs.from_date} to {delete_event_inputs.to_date} events deleting..."


@router.put("/event/status/completed")
async def update_event_completed_status(
    request:Request,
    bgt:BackgroundTasks,
    session:AsyncSession=Depends(get_db_session),
    user:dict=Depends(verify),
    event_id:str=Form(...),
    event_status:backend_enums.EventStatus=Form(...),
    feedback:str=Form(...),
    archagar:str=Form(...),
    abisegam:str=Form(...),
    helper:str=Form(...),
    poo:str=Form(...),
    read:str=Form(...),
    prepare:str=Form(...),
    image:Optional[UploadFile]=File(default=None),
    
):
    if event_status==backend_enums.EventStatus.COMPLETED:
        fields = [event_id, feedback, archagar, abisegam, helper, poo, read, prepare]

        if any(not field.strip() for field in fields):
            raise HTTPException(
                status_code=422,
                detail="input fields could not be empty"
            )
        
        
        user_id=user["id"]

        image_bytes = None
        if image:
            image_bytes = await image.read()
            if len(image_bytes) > 5*1024*1024:
                raise HTTPException(
                    status_code=422,
                    detail="image should be less than 5 mb"
                )
            
            
        asyncio.create_task(
            UpdateEventCompletedStatus(
                session=session,
                user_id=user_id,
                event_id=event_id,
                event_status=event_status,
                feedback=feedback,
                archagar=archagar,
                abisegam=abisegam,
                helper=helper,
                poo=poo,
                read=read,
                prepare=prepare,
                image_url_path=str(request.base_url)+"event/status/image/",
                image=image_bytes,
                bg_task=bgt,
                request=request
            ).update_event_status()
        )
        
        ic("odaney")
        return ORJSONResponse(
            status_code=200,
            content="Updating event status..."
        )
    raise HTTPException(
        status_code=422,
        detail=f"invalis event status,expected completed actual {event_status}".title()
    )

@router.put("/event/status/pending-canceled")
async def update_event_pending_canceled_status(request:Request,status_inp:UpdateEventPendingCanceledStatusSchema,bgt:BackgroundTasks,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    asyncio.create_task(
        UpdateEventPendingCanceledStatus(
            session=session,
            user_id=user_id,
            event_id=status_inp.event_id,
            event_status=status_inp.event_status,
            description=status_inp.status_description,
            bg_task=bgt,
            can_attach_link=status_inp.can_attach_link,
            request=request
        ).update_event_status()
    )

    ic("odaneyy")
    return ORJSONResponse(
        status_code=200,
        content="Updating event status..."
    )

@router.get("/event/status/image/{image_id}")
async def get_event_status_image(image_id:str,session:AsyncSession=Depends(get_db_session)):
    image_id=image_id.split(".")[0]
    image=await GetEventStatusImage(
        session=session,
        image_id=image_id
    ).get_image()

    return StreamingResponse(
        BytesIO(image),
        media_type="image/jpeg",
        headers={
            "Content-Disposition": f'inline; filename="{image_id}.jpg"'
        }
    )


@router.post("/event/report/email")
async def get_events_reprot_emails(event_email_inputs:GetEventsEmailschema,bgt:BackgroundTasks,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    user=await UserVerification(session=session).is_user_exists_by_id(id=user_id)
    emails=[user.email]
    if event_email_inputs.send_to!=None:
        emails.append(event_email_inputs.send_to)
    for email in emails:
        bgt.add_task(
            EventsToEmail(
                session=session,
                user_id=user_id,
                from_date=event_email_inputs.from_date,
                to_date=event_email_inputs.to_date,
                file_type=event_email_inputs.file_type,
                to_email=email
            ).get_events_email,
            user=user
        )

    # report=await EventsToEmail(
    #         session=session,
    #         user_id=user_id,
    #         from_date=event_email_inputs.from_date,
    #         to_date=event_email_inputs.to_date,
    #         file_type=event_email_inputs.file_type,
    #         to_email="siva967763@gmail.com"
    #     ).get_events_email()
    

    return "Sending event report..."

@router.post("/event/contact-description")
async def add_or_update_contact_desc(cont_desc_inp:AddContactDescriptionSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    added_updated_cont_desc=await ContactDescription(
        session=session,
        user_id=user_id
    ).add_description(event_id=cont_desc_inp.event_id,contact_description=cont_desc_inp.contact_description)

    return added_updated_cont_desc

@router.delete("/event/contact-description")
async def delete_contact_desc(cont_desc_inp:DeleteContactDescriptionSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    deleted_cont_desc=await ContactDescription(
        session=session,
        user_id=user_id
    ).delete_description(contact_desc_id=cont_desc_inp.contact_desc_id)

    return ORJSONResponse(
        status_code=200,
        content=deleted_cont_desc
    )

@router.get("/event/contact-description")
async def get_contact_desc(event_id:str=Query(...),session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    fetched_cont_desc=await ContactDescription(
        session=session,
        user_id=user_id
    ).get_description(event_id=event_id)

    return fetched_cont_desc

@router.post("/event/assign")
async def assign_worker_to_event(assign_inp:AddEventAssignmentSchema,bgt:BackgroundTasks,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    assigned=await EventAssignmentCrud(
        session=session,
        user_id=user_id
    ).add_update_event_assignment(
        bg_task=bgt,
        event_id=assign_inp.event_id,
        assigned_archagar=assign_inp.archagar,
        assigned_abisegam=assign_inp.abisegam,
        assigned_helper=assign_inp.helper,
        assigned_poo=assign_inp.poo,
        assigned_prepare=assign_inp.prepare,
        assigned_read=assign_inp.read

    )

    return ORJSONResponse(
        content=assigned
    )

@router.delete("/event/assign")
async def delete_assigned_events(assign_inp:DeleteEventAssignmentSchema,bgt:BackgroundTasks,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    deleted=await EventAssignmentCrud(
        session=session,
        user_id=user_id
    ).delete_event_assignment(event_id=assign_inp.event_id)

    return ORJSONResponse(
        content=deleted
    )

@router.get("/event/assign")
async def get_assigned_events(worker_name:Optional[str]=Query(None),session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    assigned_events=await EventAssignmentCrud(
        session=session,
        user_id=user_id
    ).get_assigned_events(worker_name=worker_name)

    return assigned_events
