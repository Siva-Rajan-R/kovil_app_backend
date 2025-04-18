from pydantic import BaseModel

class DeleteUserSchema(BaseModel):
    del_user_id:str