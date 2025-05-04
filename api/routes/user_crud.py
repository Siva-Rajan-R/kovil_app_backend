from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from database.operations.user_crud import DeleteUser,GetUsers,UpdateUser
from database.main import get_db_session
from sqlalchemy.orm import Session
from api.dependencies import token_verification
from api.schemas.user_crud import DeleteUserSchema,UpdateUserSchema
from icecream import ic
router=APIRouter(
    tags=["Get,Update And Delete Users"]
)

@router.delete("/user")
async def delete_user(delete_user_inputs:DeleteUserSchema,session:Session=Depends(get_db_session),user:dict=Depends(token_verification.verify)):
    user_id=user["id"]
    deleted_user=await DeleteUser(
        session=session,
        user_id=user_id,
        del_user_id=delete_user_inputs.del_user_id
    ).delete_user()

    return JSONResponse(
        status_code=200,
        content=deleted_user
    )

@router.get("/users")
async def get_users(session:Session=Depends(get_db_session),user:dict=Depends(token_verification.verify)):
    user_id=user["id"]
    users=await GetUsers(
        session=session,
        user_id=user_id
    ).get_users()

    return users


@router.put("/user/role")
async def delete_user(update_user_input:UpdateUserSchema,session:Session=Depends(get_db_session),user:dict=Depends(token_verification.verify)):
    user_id=user["id"]
    update_user_role=await UpdateUser(
        session=session,
        user_id=user_id
    ).update_user_role(user_id_to_update=update_user_input.user_id,role_to_update=update_user_input.role)

    return JSONResponse(
        status_code=200,
        content=update_user_role
    )