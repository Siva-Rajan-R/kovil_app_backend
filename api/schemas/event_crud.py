from pydantic import BaseModel,EmailStr
from datetime import date,time
from enums import backend_enums
from typing import Optional


class AddEventSchema(BaseModel):
    event_name:str
    event_description:str
    event_date:date
    event_start_at:time
    event_end_at:time
    client_name:str
    client_mobile_number:str
    client_email:Optional[EmailStr]
    total_amount:int
    paid_amount:int
    payment_status:backend_enums.PaymetStatus=backend_enums.PaymetStatus.NOT_PAID
    payment_mode:backend_enums.PaymentMode=backend_enums.PaymentMode.OFFLINE

class DeleteEventSchema(BaseModel):
    event_id:str

class UpdateEventStatusSchema(BaseModel):
    event_id:str
    event_status:backend_enums.EventStatus=backend_enums.EventStatus.PENDING