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

async def get_notification_image_url(session:Session,request:Request,notification_id:str,notification_title:str,notification_body:str,notification_image:bytes,compress_image:Optional[bool]=False):
    try:
        ctx = session.begin() if not session.in_transaction() else nullcontext()
        with ctx:
            ic("hello")
            compressed_bytes=notification_image
            if compress_image:
                compressed_bytes=compress_image_to_target_size(image_binary=notification_image,target_size_bytes=300*1024)

            image_id=await create_unique_id(notification_title)
            ic(f"hello {len(compressed_bytes)}")
            image_url="https://muddy-danette-sivarajan-1b1beec7.koyeb.app/"+f"notification/image/{image_id}"
            ic(image_url)
            await NotificationsCrud(
                session=session
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
                    image=compressed_bytes
                )
            )
            ic("scuccessfully notification image created")
            # str(request.base_url)
            ic(image_url)
            return image_url

            
    except Exception as e:
        ic(f"error while create notification image : {e}")
        return HTTPException(
            status_code=500,
            detail=f"error while create notification image : {e}"
        )
    