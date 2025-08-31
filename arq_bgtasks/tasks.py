from database.main import get_db_session_ctx
from database.operations.workers_crud import WorkersCrud
from database.operations.event_info import EventsToEmail
from database.operations.event_crud import UpdateEventPendingCanceledStatus,UpdateEventCompletedStatus
from fastapi import Request


async def worker_report(ctx,*,user_id:str,from_date,to_date,amount,send_to,isfor_reset:bool):
    async with get_db_session_ctx() as session:
        return await WorkersCrud(
                session=session,
                user_id=user_id,
        ).reset_all_workers(from_date=from_date,to_date=to_date,amount=amount,to_email=send_to,isfor_reset=isfor_reset)

async def events_to_email(ctx,*,user_id:str,user,from_date,to_date,file_type,to_email):
    async with get_db_session_ctx() as session:
        return await EventsToEmail(
                session=session,
                user_id=user_id,
                from_date=from_date,
                to_date=to_date,
                file_type=file_type,
                to_email=to_email
            ).get_events_email(user=user)   
    
async def event_completed_status(ctx,*,base_url:str,image_url:str,user_id:str,event_id:str,event_status:str,feedback:str=None,archagar:bool=False,abisegam:bool=False,helper:bool=False,poo:bool=False,read:bool=False,prepare:bool=False,image_bytes:bytes):
    async with get_db_session_ctx() as session:
        return await UpdateEventCompletedStatus(
                session=session,
                user_id=user_id,
                event_id=event_id,
                event_status=event_status,
                feedback=feedback,
                archagar=archagar,
                abisegam=abisegam,
                helper=helper,
                poo=poo,
                read=read,
                prepare=prepare,
                image_url_path=image_url,
                image=image_bytes,
                base_url=base_url
            ).update_event_status()
    
async def event_pending_canceled_status(ctx,*,base_url:str,user_id:str,event_id:str,event_status:str,description:str,can_attach_link:bool):
    async with get_db_session_ctx() as session:
        return await UpdateEventPendingCanceledStatus(
                session=session,
                user_id=user_id,
                event_id=event_id,
                event_status=event_status,
                description=description,
                can_attach_link=can_attach_link,
                base_url=base_url
            ).update_event_status()
