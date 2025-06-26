from fastapi import BackgroundTasks,HTTPException
from database.operations.user_auth import UserVerification
from database.models.notification import Notifications,NotificationRecivedUsers,NotificationImages
from database.models.user import Users
from database.main import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select,desc,or_,and_
from datetime import datetime,timezone,timedelta
from contextlib import nullcontext
from icecream import ic
from enums import backend_enums
import asyncio
from typing import Optional
from security.uuid_creation import create_unique_id


def delete_expired_notification():
    session = SessionLocal()
    ic("entered delete process")
    expiry_time=datetime.now(timezone.utc)-timedelta(hours=24)
    session.query(Notifications).filter(Notifications.created_at<expiry_time).delete()
    session.query(NotificationImages).filter(NotificationImages.created_at<expiry_time).delete()
    session.commit()
    ic("removed expired notifications and images")

class NotificationsCrud:
    def __init__(self,session:Session,user_id:str,is_for:Optional[str]="all"):
        self.session=session
        self.user_id=user_id
        self.is_for=is_for
    
    async def add_notification(self,notify_title:str,notify_body:str,notify_img_url:str|None=None,notify_id:Optional[str]=None):
        try:
            ctx = self.session.begin() if not self.session.in_transaction() else nullcontext()
            with ctx:
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)

                if notify_id==None:
                    notify_id=await create_unique_id(data=notify_title)

                if user.role==backend_enums.UserRole.ADMIN:
                    notify_to_add=Notifications(
                        id=notify_id,
                        title=notify_title.title(),
                        body=notify_body.title(),
                        image_url=notify_img_url,
                        is_for=self.is_for,
                        created_at=datetime.now(timezone.utc),
                        created_by=user.name
                    )

                    self.session.add(notify_to_add)

                    ic(f"successfully notification added {datetime.now(timezone.utc)}")
                    return
                raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to send notification"
                )
            
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while adding notification {e}"
            )
        
    def update_add_notify_reciv_user(self,user:Users):
        try:
            notify_recvd_user_query=self.session.query(NotificationRecivedUsers).filter(NotificationRecivedUsers.user_id==user.id)
            notify_recvd_user=notify_recvd_user_query.first()
            utc_now=datetime.now(timezone.utc)
            if notify_recvd_user:
                notify_recvd_user_query.update(
                    {
                        NotificationRecivedUsers.last_checked:utc_now
                    }
                )
            else:
                notify_user_to_add=NotificationRecivedUsers(
                    user_id=user.id,
                    last_checked=utc_now
                )
                self.session.add(
                    notify_user_to_add
                )
            self.session.commit()
            ic("notification seen updated successfully")

        except Exception as e:
            ic(f"something went wrong while updating notification seen {e}")
    
    async def get_notifications(self):
        try:
            user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
            def get_seen_notifications(last_checked):
                ic("seen function called")
                notifications=self.session.execute(
                    select(
                        Notifications.title,
                        Notifications.body,
                        Notifications.image_url,
                        Notifications.created_at,
                        Notifications.created_by
                    )
                    .where(
                        or_(
                            and_(Notifications.created_at<=last_checked,Notifications.is_for=="all"),
                            and_(Notifications.created_at<=last_checked,Notifications.is_for==user.id)
                        )
                    )
                    .order_by(desc(Notifications.created_at))
                ).mappings().all()
                return notifications
            
            def get_new_notifications(last_checked):
                ic("fucntjif ca;lled")
                notifications=self.session.execute(
                    select(
                        Notifications.title,
                        Notifications.body,
                        Notifications.image_url,
                        Notifications.created_at,
                        Notifications.created_by
                    )
                    .where(
                        or_(
                            and_(Notifications.created_at>last_checked,Notifications.is_for=='all'),
                            and_(Notifications.created_at>last_checked,Notifications.is_for==user.id)
                        )
                        
                    )
                    .order_by(desc(Notifications.created_at))
                ).mappings().all()

                return notifications
            
            def get_all_notifications():
                ic("function called")
                notifications=self.session.execute(
                    select(
                        Notifications.title,
                        Notifications.body,
                        Notifications.image_url,
                        Notifications.created_at,
                        Notifications.created_by
                    )
                    .where(
                        or_(
                            Notifications.is_for=='all',
                            Notifications.is_for==user.id
                        )
                    )
                    .order_by(desc(Notifications.created_at))
                ).mappings().all()
                return notifications

            
            last_checked=self.session.query(NotificationRecivedUsers.last_checked).filter(NotificationRecivedUsers.user_id==user.id).scalar()
            ic(last_checked)
            if not last_checked:
                tasks=[asyncio.to_thread(get_all_notifications)]
            else:
                tasks=[asyncio.to_thread(get_new_notifications,last_checked),asyncio.to_thread(get_seen_notifications,last_checked)]

            ic(tasks)
            compeleted_tasks=await asyncio.gather(*tasks)

            ic(compeleted_tasks)
            ic("hello world")
            notifications={"notifications":{"new":compeleted_tasks[0],"seen":[]}}
            if len(compeleted_tasks)==2:
                notifications['notifications']["seen"]=compeleted_tasks[1]
            return notifications
        
        except HTTPException:
            raise

        except Exception as e:
            self.session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while fetching notifications {e}"
            )