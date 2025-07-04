from fastapi import APIRouter,BackgroundTasks,Depends,Query,Request,Form,File,UploadFile,HTTPException
from fastapi.responses import StreamingResponse,ORJSONResponse,Response
import os
import orjson
from utils.push_notification import PushNotificationCrud,messaging
from utils.notification_image_url import get_notification_image_url
from security.uuid_creation import create_unique_id
from security.entity_tag import generate_entity_tag
from firebase_db.operations import FirebaseCrud
from api.schemas.application import RegisterNotifySchema,DeleteNotifySchema
from database.operations.user_auth import UserVerification
from database.operations.notification import NotificationsCrud
from dotenv import load_dotenv
from database.main import get_db_session
from database.models.notification import NotificationImages
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from icecream import ic
from io import BytesIO
from api.dependencies.token_verification import verify
from typing import Optional
from PIL import Image
from redis_db.redis_crud import RedisCrud
from redis_db.main import redis
from redis_db.redis_etag_keys import NOTIFICATION_ETAG_KEY
import asyncio
load_dotenv()


router=APIRouter(
    tags=["get the current version"]
)

version_info=os.getenv("VERSION_INFO")



@router.get("/app/version")
async def get_app_version(request:Request,response:Response):
    version=orjson.loads(version_info)
    # version={
    #     "current_version": "1.1.2",
    #     "is_debug": False,
    #     "is_mandatory": True,
    #     "is_trigger_login":False,
    #     "update_url": "https://drive.google.com/file/d/1MHXqE733vo0D1wAyMjcsG9n9BxhmETn3/view?usp=drive_link",
    #     "android_update_url": "https://drive.google.com/file/d/1MHXqE733vo0D1wAyMjcsG9n9BxhmETn3/view?usp=drive_link",
    #     "ios_update_url": "https://drive.google.com/file/d/1MHXqE733vo0D1wAyMjcsG9n9BxhmETn3/view?usp=drive_link",
    #     "windows_update_url": "https://drive.google.com/file/d/1l6CLu130rgoIfwp4C-7lxpiL6Kfejj-o/view?usp=sharing",
    #     "macos_update_url": "https://drive.google.com/file/d/1MHXqE733vo0D1wAyMjcsG9n9BxhmETn3/view?usp=drive_link"
    #     }
        
    etag=generate_entity_tag(str(version))
    if request.headers.get('if-none-match')==etag:
        raise HTTPException(
            status_code=304
        )
    
    # response.headers['ETag']=etag
    return ORJSONResponse(
        content=version,
        headers={"ETag":etag}
    )


@router.post("/app/notify/all")
async def send_app_notify(
    bgt:BackgroundTasks,
    request:Request,
    notification_title:str=Form(...,min_length=5),
    notification_body:str=Form(...,min_length=5),
    notification_image:Optional[UploadFile]=File(None),
    session:AsyncSession=Depends(get_db_session),
    verified_user:dict=Depends(verify),
):
    user_id=verified_user['id']
    image_url=None
    notify_id=await create_unique_id(data=notification_title)
    if notification_image:
        image_bytes=await notification_image.read()
        if len(image_bytes) > 400*1024:
            raise HTTPException(
            status_code=422,
            detail="notification image should be lessthan 400 kb"
        )
        
        image_url=await get_notification_image_url(
            session=session,
            request=request,
            notification_id=notify_id,
            notification_title=notification_title,
            notification_body=notification_body,
            notification_image=image_bytes,
            compress_image=False,
            user_id=user_id
        )
    else:
        await NotificationsCrud(
            session=session,
            user_id=user_id
        ).add_notification(
            notify_id=notify_id,
            notify_title=notification_title,
            notify_body=notification_body,
            notify_img_url=image_url
        )

    asyncio.create_task(
        PushNotificationCrud(
            notify_title=notification_title,
            notify_body=notification_body,
            data_payload={
                "screen":"event_page"
            }
        ).push_notification_to_all(image_url=image_url)
        
    )

    ic("immediyed")
    return "sended notification successfully"

@router.post("/app/notify/register-update")
async def register_fcm_token(request:Request,register_inp:RegisterNotifySchema,bgt:BackgroundTasks,session:AsyncSession=Depends(get_db_session)):
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

    ic("fcm token added successfuly")

@router.get("/app/notifications",response_model_exclude_none=True)
async def get_app_notifications(response:Response,request:Request,bgt:BackgroundTasks,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    
    redis_crud=RedisCrud(key=NOTIFICATION_ETAG_KEY)
    redis_etag=await redis_crud.get_etag_from_redis()
    ic(redis_etag)
    ic(redis_etag)
    if redis_etag:
        if request.headers.get('If-None-Match') == redis_etag:
            raise HTTPException(
                status_code=304
            )
    
    notifications=await NotificationsCrud(
        session=session,
        user_id=user_id
    ).get_notifications()
    
    ic(len(notifications))

    serialized_data=str(notifications)
    etag = generate_entity_tag(serialized_data)
    response.headers['ETag']=etag
    await redis_crud.store_etag_to_redis(etag=etag)
    ic(len(serialized_data))
    return notifications

@router.put("/app/notifications/seen")
async def app_notifications_seen(response:Response,request:Request,bgt:BackgroundTasks,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    try:
        user=await UserVerification(session=session).is_user_exists_by_id(user_id)
        bgt.add_task(
            NotificationsCrud(
                session=session,
                user_id=user_id
            ).update_add_notify_reciv_user,
            user=user
        )
        await RedisCrud(key=NOTIFICATION_ETAG_KEY).unlink_etag_from_redis()
        ic("notification seen updating...")
    except HTTPException:
        ic("404 user does not exists")
    
    except Exception as e:
        ic(f"something went wrong while updating notification seen {e}")


@router.delete("/app/notify/token")
async def delete_fcm_token(register_inp:DeleteNotifySchema,bgt:BackgroundTasks,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
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

    ic("notification successfully deleted")

@router.get("/notification/image/{image_id}")
async def get_notification_image(image_id:str,session:AsyncSession=Depends(get_db_session)):
    try:
        image=(await session.execute(select(NotificationImages).filter(image_id==NotificationImages.id))).scalar_one_or_none()
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
        


# async def bgt_test(msg:str,image:bytes):
#     await asyncio.sleep(10)
#     ic(f"succefully executed bgt task after 10 sec {msg} {image} recived")

# @router.get("/test-bg")
# async def test_bgt(bgt:BackgroundTasks,image:UploadFile=File(None)):
#     image_bytes=await image.read()
#     bgt.add_task(bgt_test,msg="my message",image=image_bytes)

#     return "before going to bgt is sended"