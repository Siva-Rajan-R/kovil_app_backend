from utils.image_compression import compress_image_to_target_size
from security.uuid_creation import create_unique_id
from sqlalchemy.orm import Session
from fastapi.requests import Request
from database.models.notification import NotificationImages
from icecream import ic
from contextlib import nullcontext

async def get_notification_image_url(session:Session,request:Request,notification_title:str,notification_image:bytes):
    try:
        ctx = session.begin() if not session.in_transaction() else nullcontext()
        with ctx:
            session.query(NotificationImages).delete()

            compressed_bytes=compress_image_to_target_size(image_binary=notification_image,target_size_bytes=350*1024)
            image_id=await create_unique_id(notification_title)
            ic("hello")
            session.add(
                NotificationImages(
                    id=image_id,
                    image=compressed_bytes
                )
            )
            ic("scuccessfully notification image created")
            return str(request.base_url)+f"notification/image/{image_id}"

            
    except Exception as e:
        ic(f"error while create notification image : {e}")
        return None
    