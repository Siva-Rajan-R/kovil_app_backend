from pydantic import BaseModel,EmailStr,constr
from enums import backend_enums
from typing import Optional

class UserRegisterSchema(BaseModel):
    name:constr(strip_whitespace=True,min_length=1)#type: ignore
    mobile_number:constr(strip_whitespace=True,min_length=1)#type: ignore
    email:EmailStr
    role:backend_enums.UserRole
    password:constr(strip_whitespace=True,min_length=1)#type: ignore
    fcm_token:Optional[str]=None

class UserLoginSchema(BaseModel):
    email_or_no:EmailStr|constr(strip_whitespace=True,min_length=1)#type: ignore
    password:constr(strip_whitespace=True,min_length=1)#type: ignore

class UserForgotSchema(BaseModel):
    email_or_no:EmailStr|constr(strip_whitespace=True,min_length=1)#type: ignore
    new_password:constr(strip_whitespace=True,min_length=1)#type: ignore
