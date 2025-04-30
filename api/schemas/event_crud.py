from pydantic import BaseModel,EmailStr,constr
from datetime import date,time,datetime
from enums import backend_enums
from typing import Optional


class AddEventNameSchema(BaseModel):
    event_name:constr(strip_whitespace=True,min_length=1)# type: ignore
    event_amount:int

class DeleteEventNameSchema(BaseModel):
    event_name_id:int

class AddEventSchema(BaseModel):
    event_name:constr(strip_whitespace=True,min_length=1) # type: ignore
    event_description:constr(strip_whitespace=True,min_length=1)# type: ignore
    event_date:date
    event_start_at:constr(strip_whitespace=True,min_length=1)# type: ignore
    event_end_at:constr(strip_whitespace=True,min_length=1)# type: ignore
    client_name:constr(strip_whitespace=True,min_length=1)# type: ignore
    client_mobile_number:constr(strip_whitespace=True,min_length=1)# type: ignore
    client_city:constr(strip_whitespace=True,min_length=1)# type: ignore
    total_amount:int
    paid_amount:int
    payment_status:backend_enums.PaymetStatus=backend_enums.PaymetStatus.NOT_PAID
    payment_mode:backend_enums.PaymentMode=backend_enums.PaymentMode.OFFLINE

class DeleteEventSchema(BaseModel):
    event_id:constr(strip_whitespace=True,min_length=1)# type: ignore

class UpdateEventSchema(BaseModel):
    event_id:constr(strip_whitespace=True,min_length=1) # type: ignore
    event_name:constr(strip_whitespace=True,min_length=1) # type: ignore
    event_description:constr(strip_whitespace=True,min_length=1)# type: ignore
    event_date:date
    event_start_at:constr(strip_whitespace=True,min_length=1)# type: ignore
    event_end_at:constr(strip_whitespace=True,min_length=1)# type: ignore
    client_name:constr(strip_whitespace=True,min_length=1)# type: ignore
    client_mobile_number:constr(strip_whitespace=True,min_length=1)# type: ignore
    client_city:constr(strip_whitespace=True,min_length=1)# type: ignore
    total_amount:int
    paid_amount:int
    payment_status:backend_enums.PaymetStatus
    payment_mode:backend_enums.PaymentMode
