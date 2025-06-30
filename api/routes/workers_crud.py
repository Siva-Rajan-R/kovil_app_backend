from fastapi import APIRouter,Depends,Query,Request,Response,HTTPException
from security.entity_tag import generate_entity_tag
from fastapi.responses import ORJSONResponse
from database.operations.workers_crud import WorkersCrud,AsyncSession,SendWorkerInfoAsEmail
from database.main import get_db_session
from api.dependencies.token_verification import verify
from api.schemas.workers_crud import AddWorkersSchema,DeleteWorkerSchema,ResetAllWorkersSchema,UpdateWorkerUserIdSchema
from utils.clean_ph_numbers import clean_phone_numbers
from datetime import date
from typing import Optional
from redis_db.redis_crud import RedisCrud
from icecream import ic
from redis_db.redis_etag_keys import WORKER_ETAG_KEY,WORKER_WITH_USER_ETAG_KEY


router=APIRouter(
    tags=["Add,Update and Delete Workers"]
)



@router.post("/worker")
async def add_worker(request:Request,worker_inp:AddWorkersSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']

    if len(worker_inp.worker_mobile_number)>10:
        worker_inp.worker_mobile_number=await clean_phone_numbers(worker_inp.worker_mobile_number)

    added_worker=await WorkersCrud(
        session=session,
        user_id=user_id,
        worker_name=worker_inp.worker_name
    ).add_workers(worker_mobile_number=worker_inp.worker_mobile_number,worker_user_id=worker_inp.worker_user_id)

    await RedisCrud(key="").unlink_etag_from_redis(WORKER_ETAG_KEY,WORKER_WITH_USER_ETAG_KEY)
    return ORJSONResponse(
        status_code=201,
        content=added_worker
    )

@router.put("/worker/user-id")
async def update_worker_user_id(request:Request,worker_inp:UpdateWorkerUserIdSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']

    updated_worker=await WorkersCrud(
        session=session,
        user_id=user_id,
        worker_name=worker_inp.worker_name
    ).update_worker_as_app_user(worker_user_id=worker_inp.worker_user_id)

    await RedisCrud(key="").unlink_etag_from_redis(WORKER_ETAG_KEY,WORKER_WITH_USER_ETAG_KEY)
    return ORJSONResponse(
        status_code=201,
        content=updated_worker
    )

@router.delete("/worker")
async def delete_worker(request:Request,worker_inp:DeleteWorkerSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    deleted_worker=await WorkersCrud(
        session=session,
        user_id=user_id,
        worker_name=worker_inp.worker_name
    ).delete_workers()
    
    await RedisCrud(key="").unlink_etag_from_redis(WORKER_ETAG_KEY,WORKER_WITH_USER_ETAG_KEY)
    return ORJSONResponse(
        status_code=200,
        content=deleted_worker
    )

@router.put("/worker/reset")
async def reset_worker(request:Request,worker_inp:DeleteWorkerSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    reseted_worker=await WorkersCrud(
        session=session,
        user_id=user_id,
        worker_name=worker_inp.worker_name
    ).reset_workers()
    
    await RedisCrud(key=WORKER_ETAG_KEY).unlink_etag_from_redis()
    return ORJSONResponse(
        status_code=200,
        content=reseted_worker
    )

@router.put("/worker/reset/all")
async def reset_all_worker(request:Request,worker_inp:ResetAllWorkersSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    reseted_worker=await WorkersCrud(
        session=session,
        user_id=user_id,
    ).reset_all_workers(from_date=worker_inp.from_date,to_date=worker_inp.to_date,amount=worker_inp.amount,to_email=worker_inp.send_to,isfor_reset=True)

    await RedisCrud(key=WORKER_ETAG_KEY).unlink_etag_from_redis()
    return ORJSONResponse(
        status_code=200,
        content=reseted_worker
    )

@router.post("/worker/report/email")
async def worker_report_email(worker_inp:ResetAllWorkersSchema,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    email_send=await WorkersCrud(
        session=session,
        user_id=user_id,
    ).reset_all_workers(from_date=worker_inp.from_date,to_date=worker_inp.to_date,amount=worker_inp.amount,to_email=worker_inp.send_to,isfor_reset=False)

 
    return ORJSONResponse(
        status_code=200,
        content=email_send
    )

@router.get("/workers")
async def get_worker(request:Request,response:Response,session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify),include_users:Optional[str]=Query(None)):
    user_id=user['id']
    key=WORKER_ETAG_KEY
    if include_users:
        key=WORKER_WITH_USER_ETAG_KEY
    redis_crud=RedisCrud(key=key)

    redis_etag=await redis_crud.get_etag_from_redis()
    ic(redis_etag,request.headers.get("if-none-match"))
    if redis_etag:
        if request.headers.get("if-none-match")==redis_etag:
            raise HTTPException(
                status_code=304,
            )
    
    fetched_worker=await WorkersCrud(
        session=session,
        user_id=user_id,
    ).get_workers(include_users=include_users)

    etag=generate_entity_tag(data=str(fetched_worker))
    await redis_crud.store_etag_to_redis(etag=etag)
    response.headers['ETag']=etag
    return fetched_worker

@router.get("/workers/date")
async def get_worker_by_date(from_date:date=Query(...),to_date:date=Query(...),session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    fetched_worker=await WorkersCrud(
        session=session,
        user_id=user_id,
    ).get_workers_by_date(from_date=from_date,to_date=to_date)

    return fetched_worker