from fastapi import APIRouter,Depends,Query
from fastapi.responses import JSONResponse
from database.operations.workers_crud import WorkersCrud,Session
from database.main import get_db_session
from api.dependencies.token_verification import verify
from api.schemas.workers_crud import AddWorkersSchema,DeleteWorkerSchema
from utils.clean_ph_numbers import clean_phone_numbers
from datetime import date


router=APIRouter(
    tags=["Add,Update and Delete Workers"]
)

@router.post("/worker")
async def add_worker(worker_inp:AddWorkersSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']

    if len(worker_inp.worker_mobile_number)>10:
        worker_inp.worker_mobile_number=await clean_phone_numbers(worker_inp.worker_mobile_number)

    added_worker=await WorkersCrud(
        session=session,
        user_id=user_id,
        worker_name=worker_inp.worker_name
    ).add_workers(worker_mobile_number=worker_inp.worker_mobile_number)

    return JSONResponse(
        status_code=201,
        content=added_worker
    )

@router.delete("/worker")
async def delete_worker(worker_inp:DeleteWorkerSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    deleted_worker=await WorkersCrud(
        session=session,
        user_id=user_id,
        worker_name=worker_inp.worker_name
    ).delete_workers()

    return JSONResponse(
        status_code=200,
        content=deleted_worker
    )

@router.put("/worker/reset")
async def reset_worker(worker_inp:DeleteWorkerSchema,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    reseted_worker=await WorkersCrud(
        session=session,
        user_id=user_id,
        worker_name=worker_inp.worker_name
    ).reset_workers()

    return JSONResponse(
        status_code=200,
        content=reseted_worker
    )

@router.get("/workers")
async def get_worker(session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    fetched_worker=await WorkersCrud(
        session=session,
        user_id=user_id,
    ).get_workers()

    return fetched_worker

@router.get("/workers/date")
async def get_worker_by_date(from_date:date=Query(...),to_date:date=Query(...),session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    fetched_worker=await WorkersCrud(
        session=session,
        user_id=user_id,
    ).get_workers_by_date(from_date=from_date,to_date=to_date)

    return fetched_worker