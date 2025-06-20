from fastapi import APIRouter,Depends,BackgroundTasks,Response,Request,HTTPException
from fastapi.responses import ORJSONResponse
from database.operations.user_crud import DeleteUser,GetUsers,UpdateUser
from database.main import get_db_session
from sqlalchemy.orm import Session
from api.dependencies import token_verification
from api.schemas.user_crud import DeleteUserSchema,UpdateUserSchema
from security.entity_tag import generate_entity_tag
from icecream import ic
router=APIRouter(
    tags=["Get,Update And Delete Users"]
)

@router.delete("/user")
async def delete_user(bgt:BackgroundTasks,delete_user_inputs:DeleteUserSchema,session:Session=Depends(get_db_session),user:dict=Depends(token_verification.verify)):
    user_id=user["id"]
    deleted_user=await DeleteUser(
        session=session,
        user_id=user_id,
        del_user_id=delete_user_inputs.del_user_id,
        bg_task=bgt
    ).delete_user()

    return ORJSONResponse(
        status_code=200,
        content=deleted_user
    )

@router.get("/users")
async def get_users(request:Request,response:Response,session:Session=Depends(get_db_session),user:dict=Depends(token_verification.verify)):
    user_id=user["id"]
    users=await GetUsers(
        session=session,
        user_id=user_id
    ).get_users()

    etag=generate_entity_tag(data=str(users))

    if request.headers.get("if-none-match")==etag:
        raise HTTPException(
            status_code=304,
        )
    
    response.headers['ETag']=etag
    return users


@router.put("/user/role")
async def delete_user(bgt:BackgroundTasks,update_user_input:UpdateUserSchema,session:Session=Depends(get_db_session),user:dict=Depends(token_verification.verify)):
    user_id=user["id"]
    update_user_role=await UpdateUser(
        bg_task=bgt,
        session=session,
        user_id=user_id
    ).update_user_role(user_id_to_update=update_user_input.user_id,role_to_update=update_user_input.role)

    return ORJSONResponse(
        status_code=200,
        content=update_user_role
    )