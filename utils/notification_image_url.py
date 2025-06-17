from utils.image_compression import compress_image_to_target_size
from security.uuid_creation import create_unique_id
from sqlalchemy.orm import Session
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from database.models.notification import NotificationImages
from icecream import ic
from contextlib import nullcontext
from typing import Optional
from database.operations.notification import NotificationsCrud
from datetime import datetime,timedelta,timezone

async def get_notification_image_url(session:Session,request:Request,notification_title:str,notification_image:bytes,user_id:Optional[str]=None,notification_id:Optional[str]=None,notification_body:Optional[str]=None,compress_image:Optional[bool]=False):
    try:
        ctx = session.begin() if not session.in_transaction() else nullcontext()
        with ctx:
            ic("hello")
            compressed_bytes=notification_image
            if compress_image:
                compressed_bytes=compress_image_to_target_size(image_binary=notification_image,target_size_bytes=400*1024)

            image_id=await create_unique_id(notification_title)
            ic(f"hello {len(compressed_bytes)}")
            image_url=str(request.base_url)+f"notification/image/{image_id}"
            ic(image_url)

            if notification_id and notification_body and user_id:
                await NotificationsCrud(
                    session=session,
                    user_id=user_id
                ).add_notification(
                    notify_id=notification_id,
                    notify_title=notification_title,
                    notify_body=notification_body,
                    notify_img_url=image_url
                )
                ic("hello eorld")

            session.add(
                NotificationImages(
                    notify_id=notification_id,
                    id=image_id,
                    image=compressed_bytes,
                    created_at=datetime.now(timezone.utc)
                )
            )
            ic("scuccessfully notification image created")
            # str(request.base_url)
            ic(image_url)
            return image_url

    except HTTPException:
        raise
    
    except Exception as e:
        ic(f"error while create notification image : {e}")
        return HTTPException(
            status_code=500,
            detail=f"error while create notification image : {e}"
        )
    