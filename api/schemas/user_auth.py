from pydantic import BaseModel,EmailStr
from enums import backend_enums

class UserRegisterSchema(BaseModel):
    name:str
    mobile_number:str
    email:EmailStr
    role:backend_enums.UserRole
    password:str

class UserLoginSchema(BaseModel):
    email_or_no:EmailStr|str
    password:str

class UserForgotSchema(BaseModel):
    email_or_no:EmailStr|str
    new_password:str
