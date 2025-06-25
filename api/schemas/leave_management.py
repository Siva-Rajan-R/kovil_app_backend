from pydantic import BaseModel
from typing import Optional
from datetime import date
from enums import backend_enums

class LeaveManagementAddSchema(BaseModel):
    from_date:date
    to_date:date
    reason:str

class LeaveManagementUpdatedetailsSchema(BaseModel):
    leave_id:int
    from_date:date
    to_date:date
    reason:str

class LeaveManagementUpdateStatusSchema(BaseModel):
    leave_id:int
    leave_status:backend_enums.LeaveStatus

class LeaveManagementDeleteSchema(BaseModel):
    leave_id:int