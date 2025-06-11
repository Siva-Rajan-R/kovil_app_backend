from fastapi import APIRouter,BackgroundTasks,Depends,Query,Request,Form,File,UploadFile,HTTPException
from fastapi.responses import StreamingResponse
import os
import json
from utils.push_notification import PushNotificationCrud,messaging
from utils.notification_image_url import get_notification_image_url
from firebase_db.operations import FirebaseCrud
from api.schemas.application import RegisterNotifySchema,DeleteNotifySchema
from database.operations.user_auth import UserVerification
from dotenv import load_dotenv
from database.main import get_db_session
from database.models.notification import NotificationImages
from sqlalchemy.orm import Session
from icecream import ic
from io import BytesIO
from api.dependencies.token_verification import verify
from typing import Optional
load_dotenv()


router=APIRouter(
    tags=["get the current version"]
)

version_info=os.getenv("VERSION_INFO")

@router.get("/app/version")
def get_app_version():
    return json.loads(version_info)

@router.post("/app/notify/all")
async def send_app_notify(
    bgt:BackgroundTasks,
    request:Request,
    notification_title:str=Form(...,min_length=5),
    notification_body:str=Form(...,min_length=5),
    notification_image:Optional[UploadFile]=File(None),
    session:Session=Depends(get_db_session)
):
    
    image_url=None

    if notification_image:
        image_bytes=await notification_image.read()
        if len(image_bytes) > 350*1024:
            raise HTTPException(
            status_code=422,
            detail="notification image should be lessthan 350 kb"
        )

        image_url=await get_notification_image_url(
            session=session,
            request=request,
            notification_title=notification_title,
            notification_image=image_bytes
        )
    
    bgt.add_task(
        PushNotificationCrud(
            notify_title=notification_title,
            notify_body=notification_body,
            data_payload={
                "screen":"home_page"
            }
        ).push_notification_to_all,
        image_url=image_url,
        
    )

    return "sended notification successfully"

@router.post("/app/notify/register-update")
async def register_fcm_token(request:Request,register_inp:RegisterNotifySchema,bgt:BackgroundTasks,session:Session=Depends(get_db_session)):
    user_id=None
    if register_inp.user_email_or_no:
        user=await UserVerification(session=session).is_user_exists(email_or_no=register_inp.user_email_or_no)
        user_id=user.id
    else:
        user=await verify(request=request)
        ic(user['id'])
        user_id=user['id']

    if user_id:
        bgt.add_task(
            FirebaseCrud(user_id=user_id).add_fcm_tokens,
            fcm_token=register_inp.fcm_token,
            device_id=register_inp.device_id
        )

    ic("added successfuly")

@router.delete("/app/notify/token")
async def delete_fcm_token(register_inp:DeleteNotifySchema,bgt:BackgroundTasks,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    tokens=FirebaseCrud(user_id=user_id).get_fcm_tokens()
    if tokens:
        fcm_tokens=[token for device_id,token in tokens.items()]
        ic(fcm_tokens)
        bgt.add_task(
            FirebaseCrud(user_id=user_id).delete_fcm_token,
            device_id=register_inp.device_id
        )

        messaging.unsubscribe_from_topic(tokens=fcm_tokens,topic="all")

    ic("successfully deleted")

@router.get("/notification/image/{image_id}")
async def get_notification_image(image_id:str,session:Session=Depends(get_db_session)):
    try:
        image=session.query(NotificationImages).filter(image_id==NotificationImages.id).first()

        if image:
            image_binary=image.image

            return StreamingResponse(
                content=BytesIO(image_binary),
                media_type="image/jpeg",
                headers={
                    "Content-Disposition": f'inline; filename="{image_id}.jpg"'
                }
            )
        else:
            raise HTTPException(
                status_code=404,
                detail="image not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"something went wrong while fetching image {e}"
        )
        

import time 
import asyncio
async def bgt_test(msg:str,image:bytes):
    await asyncio.sleep(10)
    ic(f"succefully executed bgt task after 10 sec {msg} {image} recived")

@router.get("/test-bg")
async def test_bgt(bgt:BackgroundTasks,image:UploadFile=File(None)):
    image_bytes=await image.read()
    bgt.add_task(bgt_test,msg="my message",image=image_bytes)

    return "before going to bgt is sended"