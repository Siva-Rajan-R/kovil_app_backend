from pydantic import BaseModel,constr
from enums import backend_enums

class AddWorkersSchema(BaseModel):
    worker_name:constr(min_length=1,strip_whitespace=True)# type: ignore
    worker_mobile_number:constr(min_length=10,strip_whitespace=True)# type: ignore

class DeleteWorkerSchema(BaseModel):
    worker_name:constr(min_length=1,strip_whitespace=True)# type: ignore