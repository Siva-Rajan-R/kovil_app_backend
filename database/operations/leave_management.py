from database.models.event import (
    Events,Clients,Payments,EventsCompletedStatus,EventsPendingCanceledStatus,EventNames,EventStatusImages,NeivethiyamNames,EventsNeivethiyam,EventsContactDescription,EventsAssignments
)
from database.models.leave_management import LeaveManagement
from database.models.user import Users
from database.models.workers import Workers,WorkersParticipationLogs
from fastapi import BackgroundTasks,Request,File,UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select,func,desc,or_,and_
from enums import backend_enums
from security.uuid_creation import create_unique_id
from datetime import date,time
from pydantic import EmailStr
from fastapi.exceptions import HTTPException
from database.operations.user_auth import UserVerification
from typing import Optional
from utils import indian_time,notification_image_url
from datetime import datetime,timezone,timedelta
from icecream import ic
from firebase_db.operations import FirebaseCrud
from utils.push_notification import PushNotificationCrud
from utils.error_notification import send_error_notification
from database.operations.notification import NotificationsCrud


class LeaveManagementCrud:
    def __init__(self,session:Session,user_id:str):
        self.session=session
        self.user_id=user_id

    async def add_leave(self,bg_task:BackgroundTasks,leave_from_date:date,leave_to_date:date,leave_reason:str):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                cur_datetime_utc=datetime.now(timezone.utc)
                leave_to_add=LeaveManagement(
                    user_id=self.user_id,
                    from_date=leave_from_date,
                    to_date=leave_to_date,
                    reason=leave_reason,
                    status=backend_enums.LeaveStatus.WAITING,
                    datetime=cur_datetime_utc

                )

                self.session.add(leave_to_add)

                admins_id=self.session.execute(select(Users.id).where(Users.role==backend_enums.UserRole.ADMIN)).scalars().all()
                for admin_id in admins_id:
                    order_dict=FirebaseCrud(user_id=admin_id).get_fcm_tokens()
                    if order_dict:
                        bg_task.add_task(
                            PushNotificationCrud(
                                notify_title="Requesting Leave",
                                notify_body=f"{user.name} requesting a leave from {leave_from_date} to {leave_to_date}",
                                data_payload={
                                    'screen':'leave_screen'
                                }
                            ).push_notifications_individually,
                            fcm_tokens=order_dict
                        )
                return "Successfully sumbitted leave request"
        except HTTPException:
            raise
        except Exception as e:
            ic(f"something went wrong while sumbitting leave {e}")
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while sumbitting leave {e}"
            )
    
    async def update_leave_details(self,leave_id:int,leave_from_date:date,leave_to_date:date,leave_reason:str):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)

                leave_to_update=self.session.query(LeaveManagement).filter(LeaveManagement.id==leave_id).update(
                    {
                        LeaveManagement.from_date:leave_from_date,
                        LeaveManagement.to_date:leave_to_date,
                        LeaveManagement.reason:leave_reason
                    }
                )

                if leave_to_update:
                    return "Leave details updated Successfully"
                
                raise HTTPException(
                    status_code=404,
                    detail="No leave details found"
                )
        except HTTPException:
            raise
        except Exception as e:
            ic(f"something went wrong while updating leave details {e}")
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while updating leave details {e}"
            )
        
    async def update_leave_status(self,bg_task:BackgroundTasks,leave_id:int,leave_status:backend_enums.LeaveStatus):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                async def update_status(can_send_notification:bool=False):
                    leave_query=self.session.query(LeaveManagement).filter(LeaveManagement.id==leave_id)
                    leave_details=leave_query.first()
                    if leave_details:
                        leave_query.update(
                            {
                                LeaveManagement.status:leave_status
                            }
                        )
                        
                        is_worker_removed=False
                        removed_attributes=[]
                        removed_events_names=[]
                        # for deleting the user assigned
                        if leave_status==backend_enums.LeaveStatus.ACCEPTED:
                            events=self.session.execute(select(Events.id,Events.name).where(Events.date>=leave_details.from_date,Events.date<=leave_details.to_date)).mappings().all()
                            user_name=self.session.query(Users.name).filter(Users.id==leave_details.user_id).scalar()
                            if events!=[] and user_name:
                                for event in events:
                                    for attribute in ['archagar','abisegam','poo','read','prepare','helper']:
                                        print(event,attribute)
                                        assigned_event=self.session.query(EventsAssignments).where(EventsAssignments.event_id==event['id']).one_or_none()
                                        if assigned_event:
                                            if getattr(assigned_event,attribute)==user_name:
                                                print("vanakam")
                                                setattr(assigned_event,attribute,None)
                                                is_worker_removed=True
                                                removed_attributes.append(attribute)
                                                if event['name'] not in removed_events_names:
                                                    removed_events_names.append(event['name'])
                        # end             

                        if can_send_notification:
                            notify_title="Leave status updated"
                            notify_body=f"{user.name} {leave_status.value} your leave request"
                            await NotificationsCrud(
                                session=self.session,
                                user_id=user.id,
                                is_for=leave_details.user_id
                            ).add_notification(
                                notify_title=notify_title,
                                notify_body=notify_body
                            )

                            user_fcm_tokens=FirebaseCrud(user_id=leave_details.user_id).get_fcm_tokens()
                            if user_fcm_tokens:
                                
                                bg_task.add_task(
                                    PushNotificationCrud(
                                        notify_title=notify_title,
                                        notify_body=notify_body,
                                        data_payload={
                                            'screen':"leave_screen"
                                        }
                                    ).push_notifications_individually,
                                    fcm_tokens=user_fcm_tokens
                                )

                            if is_worker_removed:
                                admins_id=self.session.execute(select(Users.id).where(Users.role==backend_enums.UserRole.ADMIN)).scalars().all()
                                notify_title="Reminder for assigning workers"
                                notify_body=f"Workers need to assign for the fields of {removed_attributes} to the events of {removed_events_names} on {leave_details.from_date} - {leave_details.to_date}"
                                for admin_id in admins_id:
                                    await NotificationsCrud(
                                        session=self.session,
                                        user_id=admin_id,
                                        is_for=admin_id
                                    ).add_notification(
                                        notify_title=notify_title,
                                        notify_body=notify_body
                                    )

                                    admins_fcm_tokens=FirebaseCrud(user_id=admin_id).get_fcm_tokens()
                                    if admins_fcm_tokens:
                                        bg_task.add_task(
                                            PushNotificationCrud(
                                                notify_title=notify_title,
                                                notify_body=notify_body,
                                                data_payload={
                                                    'screen':"event_screen"
                                                }
                                            ).push_notifications_individually,
                                            fcm_tokens=admins_fcm_tokens
                                        )

                        return "Leave status updated Successfully"
                        
                    raise HTTPException(
                        status_code=404,
                        detail="leave id not found"
                    )
                
                if user.role==backend_enums.UserRole.ADMIN:
                    return await update_status(can_send_notification=True)
                else:
                    if leave_status==backend_enums.LeaveStatus.REJECTED:
                        return await update_status()
                    raise HTTPException(
                        status_code=422,
                        detail="Invalid status,available status ['Rejected']"
                    )
                
        except HTTPException:
            raise
        except Exception as e:
            ic(f"something went wrong while updating leave status {e}")
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while updating leave status {e}"
            )
        
    async def delete_leave(self,leave_id):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                leave_to_delete=self.session.query(LeaveManagement).filter(LeaveManagement.id==leave_id)

                if (user.role==backend_enums.UserRole.ADMIN or (user.role==backend_enums.UserRole.USER and leave_to_delete.first().status==backend_enums.LeaveStatus.WAITING)):
                    
                    if leave_to_delete.delete():
                        return "Requestes leave deleted successfully"
                    
                    raise HTTPException(
                        status_code=404,
                        detail="Leave id not found"
                    )
                raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to make any changes"
                )
        except HTTPException:
            raise
        except Exception as e:
            ic(f"something went wrong while deleting event {e}")
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while deleting event {e}"
            )
    
    async def get_leave_details(self,all:Optional[bool]=False):
        try:
            user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
            fetched_leaves=self.session.execute(
                select(
                    LeaveManagement.id,
                    LeaveManagement.from_date,
                    LeaveManagement.to_date,
                    LeaveManagement.reason,
                    LeaveManagement.status,
                    LeaveManagement.datetime,
                    Users.name
                )
                .join(Users,Users.id==LeaveManagement.user_id,isouter=True)
                .where(
                    LeaveManagement.user_id==user.id
                )
                .order_by(
                    LeaveManagement.from_date
                )
            ).mappings().all()

            if all:
                fetched_leaves=self.session.execute(
                select(
                    LeaveManagement.id,
                    LeaveManagement.from_date,
                    LeaveManagement.to_date,
                    LeaveManagement.reason,
                    LeaveManagement.status,
                    LeaveManagement.datetime,
                    Users.name
                )
                .join(Users,Users.id==LeaveManagement.user_id,isouter=True)
                .order_by(
                    LeaveManagement.from_date
                )
            ).mappings().all()

            return {'leaves':fetched_leaves}
        except HTTPException:
            raise 
        except Exception as e:
            ic(f"something went wrong while fetching leaves {e}")
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while fetching leaves {e}"
            )


    
