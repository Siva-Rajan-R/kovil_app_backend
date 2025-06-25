from fastapi import APIRouter,Depends,Request,UploadFile,File,Form,Response,HTTPException,BackgroundTasks,Query
from enums import backend_enums
from fastapi.responses import ORJSONResponse,StreamingResponse
from database.operations.leave_management import LeaveManagementCrud,Session
from database.main import get_db_session
from api.dependencies.token_verification import verify
from api.schemas.leave_management import LeaveManagementAddSchema,LeaveManagementUpdatedetailsSchema,LeaveManagementUpdateStatusSchema,LeaveManagementDeleteSchema
from typing import Optional,List
from database.operations.user_auth import UserVerification
from security.entity_tag import generate_entity_tag
from utils.clean_ph_numbers import clean_phone_numbers
from utils.image_compression import compress_image_to_target_size
from utils.async_to_sync_bgtask import run_async_in_bg
from icecream import ic
from io import BytesIO
import asyncio


router = APIRouter(
    tags=['Leave Management Crud']
)


@router.post('/user/leave')
async def add_user_leave(bgt:BackgroundTasks,leave_inp:LeaveManagementAddSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
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

@router.put('/user/leave')
async def update_user_leave_details(bgt:BackgroundTasks,leave_inp:LeaveManagementUpdatedetailsSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
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

@router.put('/user/leave/status')
async def updaate_user_leave_status(bgt:BackgroundTasks,leave_inp:LeaveManagementUpdateStatusSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    added_leave_status=await LeaveManagementCrud(
        session=session,
        user_id=user_id
    ).update_leave_status(
        bg_task=bgt,
        leave_id=leave_inp.leave_id,
        leave_status=leave_inp.leave_status
    )

    return ORJSONResponse(
        content=added_leave_status
    )

@router.delete('/user/leave')
async def delete_user_leave(bgt:BackgroundTasks,leave_inp:LeaveManagementDeleteSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    deleted_leave=await LeaveManagementCrud(
        session=session,
        user_id=user_id
    ).delete_leave(leave_id=leave_inp.leave_id)

    return ORJSONResponse(
        content=deleted_leave
    )

@router.get("/user/leave")
async def get_user_leaves(all:Optional[bool]=False,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    fetched_leaves=await LeaveManagementCrud(
        session=session,
        user_id=user_id
    ).get_leave_details(all=all)

    return fetched_leaves