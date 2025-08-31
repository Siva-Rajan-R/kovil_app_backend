from database.models.workers import Workers,WorkersParticipationLogs
from database.models.notification import NotificationRecivedUsers
from database.models.leave_management import LeaveManagement
from database.models.user import Users
from database.models.event import Events
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,desc,or_,exists,delete,update
from sqlalchemy.exc import IntegrityError
from enums import backend_enums
from fastapi import BackgroundTasks, HTTPException
from database.operations.user_auth import UserVerification
from icecream import ic
from typing import Optional
from datetime import date
from utils import document_generator,pdf_fields
from api.dependencies import email_automation
from typing import List
from pydantic import EmailStr
import asyncio
from utils.error_notification import send_error_notification


class __WorkersCrudInputs:
    def __init__(self,session:AsyncSession,user_id:str,worker_name:Optional[str]=None):
        self.session=session
        self.user_id=user_id
        self.worker_name=worker_name


class SendWorkerInfoAsEmail:
    def __init__(self,session:AsyncSession,user_id:str,workers_info:List[dict],from_date:date,to_date:date,to_email:EmailStr,amount:int):
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
                email_automation.send_events_report_as_excel(to_email=self.to_email,events=self.workers_info['workers'],excel_filename=file_name,is_contains_image=False)
                ic("excel_success")
                file_name=f"{self.from_date}-{self.to_date}_WorkersReport.pdf"
                pdf_byte=document_generator.generate_pdf(self.workers_info,pdf_fields.workers_fields_data(self.workers_info['workers'],self.amount),is_contain_image=False)
                ic("pdf_success")
                if pdf_byte:
                    email_automation.send_event_report_as_pdf(to_email=self.to_email,pdf_bytes=pdf_byte,pdf_filename=file_name)
                ic("pdf_success")
                return "successfully sended"
            
            raise HTTPException(
                status_code=401,
                detail="you are not allowed to get this information"
            )
        except HTTPException:
            raise
        except Exception as e:
            ic(f"something went wrong while geting events for email : {e}")
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while geting events for email : {e}"
            )

class WorkersCrud(__WorkersCrudInputs):

    async def is_worker_exists_by_number_and_name(self,worker_mobile_number:str):
        if self.worker_name:
            worker=await self.session.execute(select(Workers).where(or_(Workers.mobile_number==worker_mobile_number,Workers.name==self.worker_name)))
            return worker
        
        raise HTTPException(
            status_code=422,
            detail="worker name couldn't be None"
        )
    
    async def is_worker_exists_by_name(self):
        if self.worker_name:
            worker=await self.session.execute(select(Workers).filter(Workers.name==self.worker_name))
            return worker
        raise HTTPException(
            status_code=422,
            detail="worker name couldn't be None"
        )
    
    
    async def add_workers(self,worker_mobile_number:str,worker_user_id:Optional[str]=None):
        try:
            async with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)

                if user.role==backend_enums.UserRole.ADMIN:
                    worker=await self.is_worker_exists_by_number_and_name(worker_mobile_number)
                    if worker.scalar_one_or_none():
                        raise HTTPException(
                            status_code=409,
                            detail="worker name already exists"
                        )
                    
                    worker_name_toadd=Workers(
                        name=self.worker_name,
                        mobile_number=worker_mobile_number,
                        user_id=worker_user_id
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
        
    async def update_worker_as_app_user(self,worker_user_id:Optional[str]=None):
        try:
            async with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)

                if user.role==backend_enums.UserRole.ADMIN:
                    user_to_make_worker=await UserVerification(session=self.session).is_user_exists_by_id(id=worker_user_id)
                    if user_to_make_worker:
                        worker_toupdate=update(Workers).where(Workers.name==self.worker_name).values(
                            user_id=worker_user_id,
                            name=user_to_make_worker.name,
                            mobile_number=user_to_make_worker.mobile_number
                        ).returning(Workers.name)
                        
                        result = await self.session.execute(worker_toupdate)

                        if not result.scalar_one_or_none():
                            raise HTTPException(
                                status_code=404,
                                detail="worker name not found"
                            )
                        
                        return "worker updated successfully"
                    
                    raise HTTPException(
                            status_code=404,
                            detail="Selected user id not found"
                        )
                
                raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to make any changes"
                )
            
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="worker name already exists"
            )
        
        except HTTPException:
            raise
        except Exception as e:
            ic(f"something went wrong while adding worker name {e}")
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while adding worker name {e}"
            )
    
    async def delete_workers(self):
        try:
            async with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)

                if user.role==backend_enums.UserRole.ADMIN:
                    worker_todelete=delete(Workers).where(Workers.name==self.worker_name).returning(Workers.name)
                    result=await self.session.execute(worker_todelete)

                    if not result.scalar_one_or_none():
                        raise HTTPException(
                            status_code=409,
                            detail="worker name doesn't exists"
                        )

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
            async with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)

                if user.role==backend_enums.UserRole.ADMIN:
                    worker=await self.is_worker_exists_by_name()
                    worker_info=worker.scalar_one_or_none()
                    if not worker:
                        raise HTTPException(
                            status_code=409,
                            detail="worker name doesn't exists"
                        )
                    
                    worker_log_toupdate=update(WorkersParticipationLogs).where(WorkersParticipationLogs.worker_id==worker_info.id).values(
                        is_reseted=True,
                        no_of_participation=0
                    )
                    
                    await self.session.execute(worker_log_toupdate)

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
        
    async def reset_all_workers(self,from_date:date,to_date:date,amount:int,isfor_reset:bool,to_email:Optional[EmailStr]=None):
        try:
            async with self.session.begin():
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

                        if isfor_reset:

                            worker_log_toupdate=update(
                                WorkersParticipationLogs
                            ).where(
                                WorkersParticipationLogs.event_id.in_(select(Events.id).where(Events.date.between(from_date,to_date)))
                            ).values(
                                is_reseted=True,
                                no_of_participation=0
                            )
                            await self.session.execute(worker_log_toupdate)


                            return "all worker reseted successfully"
                        
                        return "worker info email sended successfully"
                    
                    raise HTTPException(
                        status_code=404,
                        detail="None of them Participated"
                    )
                
                raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to make any changes"
                )
                    
        except HTTPException as httpe:
            ic(f"error while resting all workers : {httpe.status_code} - {httpe.detail}")
            await send_error_notification(
                user_id=self.user_id,
                error_title=f"Error Resting or downloading All Workers : {httpe.status_code}".title(),
                error_body=httpe.detail,
                notify_data_payload={"type":"error_notification","source":"reset_all_workers"}
            )

        except Exception as e:
            ic(f"something went wrong while resting all worker {e}")
            await send_error_notification(
                user_id=self.user_id,
                error_title="Error Resting or downloading All Workers : 500".title(),
                error_body=f"something went wrong while resting or downloading all worker, Please Try again later".title(),
                notify_data_payload={"type":"error_notification","source":"reset_all_workers"}
            )
        
    async def get_workers(self,include_users:Optional[str]=None):
        try:
            user = await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
            
            async def execute_select_statements(select_statement,is_scalar:bool=False):
                executed_statement=(await self.session.execute(select_statement)).mappings().all()
                if is_scalar:
                    executed_statement=(await self.session.execute(select_statement)).scalar()
                return executed_statement
            
            worker_ss = select(Workers.name)
            tot_event_ss = (
                select(func.count(Events.id).label("total_events"))
            )
            user_ss=None

            if user.role == backend_enums.UserRole.ADMIN:

                worker_ss = (
                    select(
                        Workers.name,
                        Workers.mobile_number,
                        func.coalesce(func.sum(WorkersParticipationLogs.no_of_participation), 0).label("no_of_participated_events")
                    )
                    .join(WorkersParticipationLogs, Workers.id == WorkersParticipationLogs.worker_id,isouter=True)
                    .group_by(Workers.id, Workers.name, Workers.mobile_number)
                    .order_by(Workers.name)
                )

                if include_users:
                    user_ss=(
                        select(
                            Users.id,
                            Users.name,
                            Users.role,
                            Users.mobile_number
                        )
                        .where(~exists().where(Users.id==Workers.user_id))
                    )

            tasks=[
                execute_select_statements(worker_ss),
                execute_select_statements(tot_event_ss,True) 
            ]

            if user_ss!=None:
                tasks.append(execute_select_statements(user_ss))
            
            completed_tasks=await asyncio.gather(*tasks)

            workers=completed_tasks[0]
            total_events=completed_tasks[1]
            available_users=completed_tasks[2] if user_ss!=None else []
            
            return {"workers": workers,"total_events":total_events,"available_users":available_users}
        
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

            total_events = await self.session.execute(select_statement2)
            workers = await self.session.execute(select_statement)
        
            return {"workers": workers.mappings().all(),"total_events":total_events.scalar()}
        
        except HTTPException:
            raise

        except Exception as e:
            ic(f"something went wrong while getting worker name by date {e}")
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while getting worker name by date {e}"
            )