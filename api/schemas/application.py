from pydantic import BaseModel,constr
from typing import Optional,Any

class NotifySchema(BaseModel):
    notification_title:constr(min_length=5)#type:ignore
    notification_body:constr(min_length=5)#type:ignore
    image:Optional[str]=None

class RegisterNotifySchema(BaseModel):
    device_id:constr(min_length=5)#type:ignore
    fcm_token:constr(min_length=5)#type:ignore
    user_email_or_no:Optional[constr(min_length=5)]=None#type:ignore

class DeleteNotifySchema(BaseModel):
    device_id:constr(min_length=5)#type:ignore