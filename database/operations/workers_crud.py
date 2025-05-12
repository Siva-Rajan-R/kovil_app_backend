from database.models.workers import Workers,WorkersParticipationLogs
from database.models.event import Events
from sqlalchemy.orm import Session
from sqlalchemy import select,func,desc,or_
from enums import backend_enums
from fastapi.exceptions import HTTPException
from database.operations.user_auth import UserVerification
from icecream import ic
from typing import Optional
from datetime import date
from utils import document_generator,pdf_fields
from api.dependencies import email_automation
from typing import List
from pydantic import EmailStr


class __WorkersCrudInputs:
    def __init__(self,session:Session,user_id:str,worker_name:Optional[str]=None):
        self.session=session
        self.user_id=user_id
        self.worker_name=worker_name


class SendWorkerInfoAsEmail:
    def __init__(self,session:Session,user_id:str,workers_info:List[dict],from_date:date,to_date:date,to_email:EmailStr,amount:int):
        self.session=session
        self.user_id=user_id
        self.workers_info=workers_info
        self.from_date=from_date
        self.to_date=to_date
        self.to_email=to_email
        self.amount=amount

    async def send_worker_info(self):
        try:
            user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
            if user.role==backend_enums.UserRole.ADMIN:
                
                file_name=f"{self.from_date}-{self.to_date}_WorkersReport.xlsx"
                await email_automation.send_events_report_as_excel(to_email=self.to_email,events=self.workers_info['workers'],excel_filename=file_name,is_contains_image=False)
                ic("excel_success")
                file_name=f"{self.from_date}-{self.to_date}_WorkersReport.pdf"
                pdf_byte=await document_generator.generate_pdf(self.workers_info,pdf_fields.workers_fields_data(self.workers_info['workers'],self.amount),is_contain_image=False)
                ic("pdf_success")
                if pdf_byte:
                    await email_automation.send_event_report_as_pdf(to_email=self.to_email,pdf_bytes=pdf_byte,pdf_filename=file_name)
                ic("pdf_success")
                return "successfully sended"
            
            raise HTTPException(
                status_code=401,
                detail="you are not allowed to get this information"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while geting events for email : {e}"
            )

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
                detail=f"something went wrong while deleting worker name {e}"
            )
    async def reset_workers(self):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)

                if user.role==backend_enums.UserRole.ADMIN:
                    worker_query=await self.is_worker_exists_by_name()
                    worker=worker_query.one_or_none()
                    if not worker:
                        raise HTTPException(
                            status_code=409,
                            detail="worker name doesn't exists"
                        )
                    
                    self.session.query(
                        WorkersParticipationLogs
                    ).filter(
                        WorkersParticipationLogs.worker_id==worker.id
                    ).delete()

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
                detail=f"something went wrong while resting worker {e}"
            )
        
    async def reset_all_workers(self,from_date:date,to_date:date,amount:int,to_email:Optional[EmailStr]):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)

                if user.role==backend_enums.UserRole.ADMIN:
                    
                    workers_info=await self.get_workers_by_date(from_date=from_date,to_date=to_date,isfor_email=True,amount=amount)
                    ic(workers_info)
                    emails=[user.email]
                    if workers_info['workers']!=[]:
                        if to_email:
                            emails.append(to_email)

                        for email in emails:
                            await SendWorkerInfoAsEmail(
                                session=self.session,
                                user_id=self.user_id,
                                workers_info=workers_info,
                                from_date=from_date,
                                to_date=to_date,
                                to_email=email,
                                amount=amount
                            ).send_worker_info()

                        # Step 1: Get the IDs of the logs to be deleted
                        log_ids = self.session.query(WorkersParticipationLogs.id).join(
                            Events, WorkersParticipationLogs.event_id == Events.id
                        ).filter(
                            Events.date.between(from_date, to_date)
                        ).all()

                        # Step 2: Delete the logs using the IDs
                        if log_ids:
                            self.session.query(WorkersParticipationLogs).filter(
                                WorkersParticipationLogs.id.in_([log.id for log in log_ids])
                            ).delete(synchronize_session=False)


                        return "all worker reseted successfully"
                    raise HTTPException(
                        status_code=404,
                        detail="None of them Participated"
                    )
                
                raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to make any changes"
                )
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while resting all worker {e}"
            )
        
    async def get_workers(self):
        try:
            with self.session.begin():
                user = await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
                
                # Base query to select worker names
                select_statement = select(Workers.name)
                
                # If user is an admin, include mobile number and participation count
                if user.role == backend_enums.UserRole.ADMIN:
                    select_statement = (
                        select(
                            Workers.name,
                            Workers.mobile_number,
                            func.coalesce(func.sum(WorkersParticipationLogs.no_of_participation), 0).label("no_of_participated_events")
                        )
                        .join(WorkersParticipationLogs, Workers.id == WorkersParticipationLogs.worker_id,isouter=True)
                        .group_by(Workers.id, Workers.name, Workers.mobile_number)
                        .order_by(Workers.name)
                    )

                # Execute the query and fetch results
                workers = self.session.execute(select_statement).mappings().all()
                return {"workers": workers}
            
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while getting worker name {e}"
            )
        
    async def get_workers_by_date(self,from_date:date,to_date:date,isfor_email:bool=False,amount:int=0):
        try:
            user = await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
            
            # Base query to select worker names
            select_statement = select(Workers.name)
            
            # If user is an admin, include mobile number and participation count
            if user.role == backend_enums.UserRole.ADMIN:
                if isfor_email:
                    select_statement = (
                        select(
                            Workers.name,
                            Workers.mobile_number,
                            func.coalesce(func.sum(WorkersParticipationLogs.no_of_participation), 0).label("no_of_participated_events"),
                            func.coalesce(func.sum(WorkersParticipationLogs.no_of_participation)*amount, 0).label("total_amount")
                        )
                        .outerjoin(WorkersParticipationLogs, Workers.id == WorkersParticipationLogs.worker_id)  # Keep all workers
                        .outerjoin(Events, WorkersParticipationLogs.event_id == Events.id)
                        .where(
                            Events.date.between(from_date, to_date)
                        ) 
                        .group_by(Workers.id, Workers.name, Workers.mobile_number)
                        .order_by(Workers.name)
                    )
                else:
                    select_statement = (
                        select(
                            Workers.name,
                            Workers.mobile_number,
                            func.coalesce(func.sum(WorkersParticipationLogs.no_of_participation), 0).label("no_of_participated_events"),
                        )
                        .outerjoin(WorkersParticipationLogs, Workers.id == WorkersParticipationLogs.worker_id)  # Keep all workers
                        .outerjoin(Events, WorkersParticipationLogs.event_id == Events.id)
                        .where(
                            Events.date.between(from_date, to_date)
                        ) 
                        .group_by(Workers.id, Workers.name, Workers.mobile_number)
                        .order_by(Workers.name)
                    )

            # Execute the query and fetch results
            select_statement2 = (
                select(func.count(Events.id).label("total_events"))
                .where(Events.date.between(from_date, to_date))
            )

            total_events = self.session.execute(select_statement2).scalar()
            workers = self.session.execute(select_statement).mappings().all()
        
            return {"workers": workers,"total_events":total_events}
        
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while getting worker name by date {e}"
            )