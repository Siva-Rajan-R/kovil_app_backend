from fastapi import APIRouter,Depends,Request,UploadFile,File,Form,Response,HTTPException,BackgroundTasks,Query
from enums import backend_enums
from fastapi.responses import ORJSONResponse,StreamingResponse
from database.operations.leave_management import LeaveManagementCrud,AsyncSession
from database.main import get_db_session
from api.dependencies.token_verification import verify
from api.schemas.leave_management import LeaveManagementAddSchema,LeaveManagementUpdatedetailsSchema,LeaveManagementUpdateStatusSchema,LeaveManagementDeleteSchema
from typing import Optional,List
from database.operations.user_auth import UserVerification
from security.entity_tag import generate_entity_tag
from utils.clean_ph_numbers import clean_phone_numbers
from utils.image_compression import compress_image_to_target_size
from utils.async_to_sync_bgtask import run_async_in_bg
from redis_db.redis_crud import RedisCrud
from redis_db.redis_etag_keys import USER_LEAVE_ALL
from icecream import ic
from io import BytesIO
import asyncio


router = APIRouter(
    tags=['Leave Management Crud'],
    prefix="/user"
)


@router.post('/leave')
async def add_user_leave(bgt:BackgroundTasks,leave_inp:LeaveManagementAddSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    added_leave=await LeaveManagementCrud(
        session=session,
        user_id=user_id
    ).add_leave(
        bg_task=bgt,
        leave_from_date=leave_inp.from_date,
        leave_to_date=leave_inp.to_date,
        leave_reason=leave_inp.reason
    )

    return ORJSONResponse(
        content=added_leave,
        status_code=201
    )

@router.put('/leave')
async def update_user_leave_details(bgt:BackgroundTasks,leave_inp:LeaveManagementUpdatedetailsSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    updated_leave=await LeaveManagementCrud(
        session=session,
        user_id=user_id
    ).update_leave_details(
        leave_id=leave_inp.leave_id,
        leave_from_date=leave_inp.from_date,
        leave_to_date=leave_inp.to_date,
        leave_reason=leave_inp.reason
    )

    return ORJSONResponse(
        content=updated_leave
    )

@router.put('/leave/status')
async def updaate_user_leave_status(bgt:BackgroundTasks,leave_inp:LeaveManagementUpdateStatusSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    asyncio.create_task(
        LeaveManagementCrud(
            session=session,
            user_id=user_id
        ).update_leave_status(
            bg_task=bgt,
            leave_id=leave_inp.leave_id,
            leave_status=leave_inp.leave_status
        )
    )

    return ORJSONResponse(
        content="Updating Leave Status..."
    )

@router.delete('/leave')
async def delete_user_leave(bgt:BackgroundTasks,leave_inp:LeaveManagementDeleteSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    deleted_leave=await LeaveManagementCrud(
        session=session,
        user_id=user_id
    ).delete_leave(leave_id=leave_inp.leave_id)

    return ORJSONResponse(
        content=deleted_leave
    )

@router.get("/leave")
async def get_user_leaves(request:Request,response:Response,all:Optional[bool]=False,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    key=f"user-leave-{user_id}-etag"
    if all:
        key=USER_LEAVE_ALL
    redis_crud=RedisCrud(key=key)
    redis_etag=await redis_crud.get_etag_from_redis()
    if redis_etag:
        if request.headers.get('if-none-match')==redis_etag:
            raise HTTPException(
                status_code=304
            )

    fetched_leaves=await LeaveManagementCrud(
        session=session,
        user_id=user_id
    ).get_leave_details(all=all)
    etag=generate_entity_tag(str(fetched_leaves))
    response.headers['ETag']=etag
    await redis_crud.store_etag_to_redis(etag=etag)
    return fetched_leaves