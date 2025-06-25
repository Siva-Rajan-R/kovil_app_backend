from pydantic import BaseModel,EmailStr,constr
from datetime import date
from enums import backend_enums
from typing import Optional


class AddEventNameSchema(BaseModel):
    event_name:constr(strip_whitespace=True,min_length=1)# type: ignore
    event_amount:int
    is_special:bool

class AddNeivethiyamNameSchema(BaseModel):
    neivethiyam_name:constr(strip_whitespace=True,min_length=1)# type: ignore
    neivethiyam_amount:int

class DeleteEventNameSchema(BaseModel):
    event_name:str

class DeleteNeivethiyamNameSchema(BaseModel):
    neivethiyam_name:str

class AddEventSchema(BaseModel):
    event_name:constr(strip_whitespace=True,min_length=1) # type: ignore
    event_description:constr(strip_whitespace=True,min_length=1)# type: ignore
    event_date:date
    event_start_at:constr(strip_whitespace=True,min_length=1)# type: ignore
    event_end_at:constr(strip_whitespace=True,min_length=1)# type: ignore
    client_name:constr(strip_whitespace=True,min_length=1)# type: ignore
    client_mobile_number:constr(strip_whitespace=True,min_length=1)# type: ignore
    client_city:constr(strip_whitespace=True,min_length=1)# type: ignore
    total_amount:float
    paid_amount:float
    payment_status:backend_enums.PaymetStatus=backend_enums.PaymetStatus.NOT_PAID
    payment_mode:backend_enums.PaymentMode=backend_enums.PaymentMode.OFFLINE
    neivethiyam_id:Optional[int]=None
    is_special:Optional[bool]=None
    neivethiyam_kg:Optional[float]=None

class DeleteSingleEventSchema(BaseModel):
    event_id:constr(strip_whitespace=True,min_length=1)# type: ignore

class DeleteAllEventSchema(BaseModel):
    from_date:date
    to_date:date

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
    neivethiyam_id:Optional[int]=None
    is_special:bool | None
    neivethiyam_kg:int

class UpdateEventPendingCanceledStatusSchema(BaseModel):
    status_description:constr(strip_whitespace=True,min_length=5)# type: ignore
    event_id:constr(strip_whitespace=True,min_length=1) # type: ignore
    event_status:backend_enums.EventStatus

class GetEventsEmailschema(BaseModel):
    from_date:date
    to_date:date
    file_type:backend_enums.FileType
    send_to:Optional[EmailStr]=None

class AddContactDescriptionSchema(BaseModel):
    event_id:constr(strip_whitespace=True,min_length=1) # type: ignore
    contact_description:constr(strip_whitespace=True,min_length=2) # type: ignore

class DeleteContactDescriptionSchema(BaseModel):
    contact_desc_id:int

class AddEventAssignmentSchema(BaseModel):
    event_id:str
    archagar:str
    abisegam:str
    helper:str
    poo:str
    read:str
    prepare:str

class DeleteEventAssignmentSchema(BaseModel):
    event_id:str
