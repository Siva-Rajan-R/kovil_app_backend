from pydantic import BaseModel,EmailStr
from datetime import date,time
from enums import backend_enums


class AddEventNameSchema(BaseModel):
    event_name:str
    event_amount:int

class DeleteEventNameSchema(BaseModel):
    event_name_id:int

class AddEventSchema(BaseModel):
    event_name:str
    event_description:str
    event_date:date
    event_start_at:time
    event_end_at:time
    client_name:str
    client_mobile_number:str
    client_city:str
    total_amount:int
    paid_amount:int
    payment_status:backend_enums.PaymetStatus=backend_enums.PaymetStatus.NOT_PAID
    payment_mode:backend_enums.PaymentMode=backend_enums.PaymentMode.OFFLINE

class DeleteEventSchema(BaseModel):
    event_id:str
