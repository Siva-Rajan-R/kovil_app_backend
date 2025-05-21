from pydantic import BaseModel,constr,EmailStr
from typing import Optional
from datetime import date


class AddWorkersSchema(BaseModel):
    worker_name:constr(min_length=1,strip_whitespace=True)# type: ignore
    worker_mobile_number:constr(min_length=10,strip_whitespace=True)# type: ignore

class DeleteWorkerSchema(BaseModel):
    worker_name:constr(min_length=1,strip_whitespace=True)# type: ignore

class ResetAllWorkersSchema(BaseModel):
    from_date:date
    to_date:date
    amount:int
    send_to:Optional[EmailStr]=None