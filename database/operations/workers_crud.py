from database.models.workers import Workers
from sqlalchemy.orm import Session
from sqlalchemy import select,func,desc,or_
from enums import backend_enums
from fastapi.exceptions import HTTPException
from database.operations.user_auth import UserVerification
from icecream import ic
from typing import Optional


class __WorkersCrudInputs:
    def __init__(self,session:Session,user_id:str,worker_name:Optional[str]=None):
        self.session=session
        self.user_id=user_id
        self.worker_name=worker_name


class WorkersCrud(__WorkersCrudInputs):

    async def is_worker_exists_by_number_and_name(self,worker_mobile_number:str):
        if self.worker_name:
            worker=self.session.query(Workers).filter(or_(Workers.mobile_number==worker_mobile_number,Workers.name==self.worker_name))
            return worker
        
        raise HTTPException(
            status_code=422,
            detail="worker name couldn't be None"
        )
    
    async def is_worker_exists_by_name(self):
        if self.worker_name:
            worker=self.session.query(Workers).filter(Workers.name==self.worker_name)
            return worker
        raise HTTPException(
            status_code=422,
            detail="worker name couldn't be None"
        )
    
    async def add_workers(self,worker_mobile_number:str):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)

                if user.role==backend_enums.UserRole.ADMIN:
                    worker=await self.is_worker_exists_by_number_and_name(worker_mobile_number)
                    if worker.one_or_none():
                        raise HTTPException(
                            status_code=409,
                            detail="worker name already exists"
                        )
                    
                    worker_name_toadd=Workers(
                        name=self.worker_name,
                        mobile_number=worker_mobile_number
                    )

                    self.session.add(worker_name_toadd)
                    return "worker name added successfully"
                
                raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to make any changes"
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while adding worker name {e}"
            )
    
    async def delete_workers(self):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)

                if user.role==backend_enums.UserRole.ADMIN:
                    worker=await self.is_worker_exists_by_name()
                    if not worker.one_or_none():
                        raise HTTPException(
                            status_code=409,
                            detail="worker name doesn't exists"
                        )
                    
                    self.session.delete(worker.first())

                    return "worker name deleted successfully"
                
                raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to make any changes"
                )
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"some thing went wrong while deleting worker name {e}"
            )
    async def reset_workers(self):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)

                if user.role==backend_enums.UserRole.ADMIN:
                    worker=await self.is_worker_exists_by_name()
                    if not worker.one_or_none():
                        raise HTTPException(
                            status_code=409,
                            detail="worker name doesn't exists"
                        )
                    
                    worker.update(
                        {
                            Workers.no_of_participated_events:0
                        }
                    )

                    return "worker reseted successfully"
                
                raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to make any changes"
                )
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"some thing went wrong while resting worker {e}"
            )
        
    async def get_workers(self):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
                select_statement=select(Workers.name)

                if user.role==backend_enums.UserRole.ADMIN:
                    select_statement=select(Workers.name,Workers.mobile_number,Workers.no_of_participated_events)

                workers=self.session.execute(
                    select_statement.order_by(Workers.name)
                ).mappings().all()
                    

                return {"workers":workers}
            
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"some thins went wrong while deleting worker name {e}"
            )