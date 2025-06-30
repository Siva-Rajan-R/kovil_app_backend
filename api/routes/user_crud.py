from fastapi import APIRouter,Depends,BackgroundTasks,Response,Request,HTTPException
from fastapi.responses import ORJSONResponse
from database.operations.user_crud import DeleteUser,GetUsers,UpdateUser
from database.main import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from api.dependencies import token_verification
from api.schemas.user_crud import DeleteUserSchema,UpdateUserSchema
from security.entity_tag import generate_entity_tag
from redis_db.redis_crud import RedisCrud
from icecream import ic
from redis_db.redis_etag_keys import USER_ETAG_KEY

router=APIRouter(
    tags=["Get,Update And Delete Users"]
)



@router.delete("/user")
async def delete_user(request:Request,bgt:BackgroundTasks,delete_user_inputs:DeleteUserSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(token_verification.verify)):
    user_id=user["id"]
    deleted_user=await DeleteUser(
        session=session,
        user_id=user_id,
        del_user_id=delete_user_inputs.del_user_id,
        bg_task=bgt
    ).delete_user()
    await RedisCrud(key=USER_ETAG_KEY).unlink_etag_from_redis()
    return ORJSONResponse(
        status_code=200,
        content=deleted_user
    )

@router.get("/users")
async def get_users(request:Request,response:Response,session:AsyncSession=Depends(get_db_session),user:dict=Depends(token_verification.verify)):
    user_id=user["id"]
    redis_crud=RedisCrud(key=USER_ETAG_KEY)
    redis_etag=await redis_crud.get_etag_from_redis()
    ic(redis_etag)
    
    if redis_etag:
        if request.headers.get("if-none-match")==redis_etag:
            raise HTTPException(
                status_code=304,
            )
    
    users=await GetUsers(
        session=session,
        user_id=user_id
    ).get_users()

    etag=generate_entity_tag(data=str(users))
    await redis_crud.store_etag_to_redis(etag=etag)
    response.headers['ETag']=etag
    return users


@router.put("/user/role")
async def delete_user(request:Request,bgt:BackgroundTasks,update_user_input:UpdateUserSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(token_verification.verify)):
    user_id=user["id"]
    update_user_role=await UpdateUser(
        bg_task=bgt,
        session=session,
        user_id=user_id
    ).update_user_role(user_id_to_update=update_user_input.user_id,role_to_update=update_user_input.role)

    await RedisCrud(key=USER_ETAG_KEY).unlink_etag_from_redis()
    return ORJSONResponse(
        status_code=200,
        content=update_user_role
    )