from fastapi import APIRouter,Depends,Request,UploadFile,File,Form,Response,HTTPException,BackgroundTasks,Query
from enums import backend_enums
from fastapi.responses import JSONResponse
from database.operations.event_crud import AddEvent,DeleteEvent,UpdateEvent,UpdateEventStatus,Session,EventNameAndAmountCrud,GetEventStatusImage,NeivethiyamNameAndAmountCrud,ContactDescription
from database.operations.event_info import EventsToEmail
from database.main import get_db_session
from api.dependencies.token_verification import verify
from api.schemas.event_crud import AddEventSchema,UpdateEventSchema,DeleteAllEventSchema,DeleteSingleEventSchema,AddEventNameSchema,DeleteEventNameSchema,GetEventsEmailschema,AddNeivethiyamNameSchema,DeleteNeivethiyamNameSchema,AddContactDescriptionSchema,DeleteContactDescriptionSchema
from typing import Optional,List
from database.operations.user_auth import UserVerification
from utils.clean_ph_numbers import clean_phone_numbers

router=APIRouter(
    tags=["Add,Update and Delete Events and EventName"]
)

@router.get("/event/name")
async def get_event_name_and_amount(session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    event_names=await EventNameAndAmountCrud(
        session=session,
        user_id=user_id
    ).get_event_name_and_amount()

    return event_names

@router.post("/event/name")
async def add_event_name_and_amount(event_name_inp:AddEventNameSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    added_event_name=await EventNameAndAmountCrud(
        session=session,
        user_id=user_id
    ).add_event_name_and_amt(event_name=event_name_inp.event_name,event_amount=event_name_inp.event_amount)

    return JSONResponse(
        status_code=201,
        content=added_event_name
    )

@router.delete("/event/name")
async def delete_event_name_and_amount(en_del_inp:DeleteEventNameSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    added_event_name=await EventNameAndAmountCrud(
        session=session,
        user_id=user_id
    ).delete_event_name_and_amount(event_name_id=en_del_inp.event_name_id)

    return JSONResponse(
        status_code=200,
        content=added_event_name
    )

#neivethiyam
@router.get("/neivethiyam/name")
async def get_neivethiyam_name_and_amount(session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    neivethiyam_names=await NeivethiyamNameAndAmountCrud(
        session=session,
        user_id=user_id
    ).get_neivethiyam_name_and_amount()

    return neivethiyam_names

@router.post("/neivethiyam/name")
async def add_neivethiyam_name_and_amount(neivethiyam_name_inp:AddNeivethiyamNameSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    added_neivethiyam_name=await NeivethiyamNameAndAmountCrud(
        session=session,
        user_id=user_id
    ).add_neivethiyam_name_and_amt(neivethiyam_name=neivethiyam_name_inp.neivethiyam_name,neivethiyam_amount=neivethiyam_name_inp.neivethiyam_amount)

    return JSONResponse(
        status_code=201,
        content=added_neivethiyam_name
    )

@router.delete("/neivethiyam/name")
async def delete_neivethiyam_name_and_amount(en_del_inp:DeleteNeivethiyamNameSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    added_neivethiyam_name=await NeivethiyamNameAndAmountCrud(
        session=session,
        user_id=user_id
    ).delete_neivethiyam_name_and_amount(neivethiyam_name_id=en_del_inp.neivethiyam_name_id)

    return JSONResponse(
        status_code=200,
        content=added_neivethiyam_name
    )

@router.post("/event")
async def add_event(add_event_inputs:AddEventSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user["id"]
    print(add_event_inputs.neivethiyam_id)
    if len(add_event_inputs.client_mobile_number)>10:
        add_event_inputs.client_mobile_number=await clean_phone_numbers(add_event_inputs.client_mobile_number)
    print(add_event_inputs.client_mobile_number)
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
        neivethiyam_id=add_event_inputs.neivethiyam_id
    ).add_event()

    return JSONResponse(
        status_code=201,
        content=added_event
    )

@router.put("/event")
async def update_event(update_event_inputs:UpdateEventSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user["id"]
    if len(update_event_inputs.client_mobile_number)>10:
        update_event_inputs.client_mobile_number=await clean_phone_numbers(update_event_inputs.client_mobile_number)
        
    updated_event=await UpdateEvent(
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
        total_amount=update_event_inputs.total_amount,
        paid_amount=update_event_inputs.paid_amount,
        payment_status=update_event_inputs.payment_status,
        payment_mode=update_event_inputs.payment_mode,
        neivethiyam_id=update_event_inputs.neivethiyam_id
    ).update_event(event_id=update_event_inputs.event_id)

    return JSONResponse(
        status_code=200,
        content=updated_event
    )

@router.delete("/event")
async def delete_single_event(delete_event_inputs:DeleteSingleEventSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user["id"]
    deleted_event=await DeleteEvent(
        session=session,
        user_id=user_id
    ).delete_single_event(event_id=delete_event_inputs.event_id)

    return JSONResponse(
        status_code=200,
        content=deleted_event
    )

@router.delete("/event/all")
async def delete_all_event(bgt:BackgroundTasks,delete_event_inputs:DeleteAllEventSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user["id"]
    bgt.add_task(
        DeleteEvent(
        session=session,
        user_id=user_id
        ).delete_all_event,
        from_date=delete_event_inputs.from_date,
        to_date=delete_event_inputs.to_date
    )

    return f"{delete_event_inputs.from_date} to {delete_event_inputs.to_date} events deleting..."

@router.put("/event/status")
async def update_event_status(
    request:Request,
    session:Session=Depends(get_db_session),
    user:dict=Depends(verify),
    event_id:str=Form(...),
    event_status:backend_enums.EventStatus=Form(backend_enums.EventStatus.PENDING),
    feedback:str=Form(...),
    archagar:str=Form(...),
    abisegam:str=Form(...),
    helper:str=Form(...),
    poo:str=Form(...),
    read:str=Form(...),
    prepare:str=Form(...),
    image:Optional[UploadFile]=File(default=None),
    selected_workers_id:List[int] = Form(...)
    
):
    fields = [event_id, feedback, archagar, abisegam, helper, poo, read, prepare]
    
    if any(not field.strip() for field in fields) and event_status!="" and len(selected_workers_id)!=6:
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
        archagar=archagar,
        abisegam=abisegam,
        helper=helper,
        poo=poo,
        read=read,
        prepare=prepare,
        selected_workers_id=selected_workers_id,
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


@router.post("/event/report/email")
async def get_events_reprot_emails(event_email_inputs:GetEventsEmailschema,bgt:BackgroundTasks,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
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
            ).get_events_email
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
async def add_or_update_contact_desc(cont_desc_inp:AddContactDescriptionSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    added_updated_cont_desc=await ContactDescription(
        session=session,
        user_id=user_id
    ).add_description(event_id=cont_desc_inp.event_id,contact_description=cont_desc_inp.contact_description)

    return added_updated_cont_desc

@router.delete("/event/contact-description")
async def delete_contact_desc(cont_desc_inp:DeleteContactDescriptionSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    deleted_cont_desc=await ContactDescription(
        session=session,
        user_id=user_id
    ).delete_description(contact_desc_id=cont_desc_inp.contact_desc_id)

    return JSONResponse(
        status_code=200,
        content=deleted_cont_desc
    )

@router.get("/event/contact-description")
async def get_contact_desc(event_id:str=Query(...),session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    fetched_cont_desc=await ContactDescription(
        session=session,
        user_id=user_id
    ).get_description(event_id=event_id)

    return fetched_cont_desc