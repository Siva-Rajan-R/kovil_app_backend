from pydantic import BaseModel,constr

class DeleteUserSchema(BaseModel):
    del_user_id:constr(strip_whitespace=True,min_length=1)#type: ignore