from database.models.workers import Workers
from sqlalchemy.orm import Session
from sqlalchemy import select,func,desc
from enums import backend_enums
from fastapi.exceptions import HTTPException
from database.operations.user_auth import UserVerification
from icecream import ic


class __WorkersCrudInputs:
    def __init__(self,session:Session,user_id:str):
        self.session=session
        self.user_id=user_id


class WorkersCrud(__WorkersCrudInputs):

    async def is_worker_exists_by_number(self,worker_mobile_number:str):
        worker=self.session.query(Workers).filter(Workers.mobile_number==worker_mobile_number)
        return worker

    async def add_workers(self,worker_name:str,worker_mobile_number:str):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)

                if user.role==backend_enums.UserRole.ADMIN:
                    worker=await self.is_worker_exists_by_number(worker_mobile_number)
                    if worker.one_or_none():
                        raise HTTPException(
                            status_code=409,
                            detail="worker name already exists"
                        )
                    
                    worker_name_toadd=Workers(
                        name=worker_name,
                        mobile_number=worker_mobile_number
                    )

                    self.session.add(worker_name_toadd)
                    return "worker name added successfully created"
                
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
    
    async def delete_workers(self,worker_mobile_number:str):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)

                if user.role==backend_enums.UserRole.ADMIN:
                    worker=await self.is_worker_exists_by_number(worker_mobile_number)
                    if not worker.one_or_none():
                        raise HTTPException(
                            status_code=409,
                            detail="worker name doesn't exists"
                        )
                    
                    worker.delete()

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
                detail=f"some thins went wrong while deleting worker name {e}"
            )
    
    async def get_workers(self):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
                select_statement=select(Workers.id,Workers.name)

                if user.role==backend_enums.UserRole.ADMIN:
                    select_statement=select(Workers.id,Workers.name,Workers.mobile_number,Workers.no_of_participated_events)

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