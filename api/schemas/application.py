from pydantic import BaseModel,constr

class NotifySchema(BaseModel):
    notification_title:constr(min_length=5)#type:ignore
    notification_body:constr(min_length=5)#type:ignore