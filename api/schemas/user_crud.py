from pydantic import BaseModel,constr
from enums import backend_enums

class DeleteUserSchema(BaseModel):
    del_user_id:constr(strip_whitespace=True,min_length=1)#type: ignore

class UpdateUserSchema(BaseModel):
    user_id:constr(strip_whitespace=True,min_length=1)#type: ignore
    role:backend_enums.UserRole