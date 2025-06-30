from fastapi import BackgroundTasks,HTTPException
from database.operations.user_auth import UserVerification
from database.models.notification import Notifications,NotificationRecivedUsers,NotificationImages
from database.models.user import Users
from database.main import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,desc,or_,and_,delete
from datetime import datetime,timezone,timedelta
from contextlib import nullcontext
from icecream import ic
from enums import backend_enums
import asyncio
from typing import Optional
from utils.db_transaction_management import maybe_begin
from security.uuid_creation import create_unique_id

async def delete_expired_notification():
    session = SessionLocal()
    async with session.begin():
        ic("entered delete process")
        expiry_time=datetime.now(timezone.utc)-timedelta(hours=24)
        await session.execute(delete(Notifications).where(Notifications.created_at<expiry_time))
        await session.execute(delete(NotificationImages).where(NotificationImages.created_at<expiry_time))
        ic("removed expired notifications and images")

class NotificationsCrud:
    def __init__(self,session:AsyncSession,user_id:str,is_for:Optional[str]="all"):
        self.session=session
        self.user_id=user_id
        self.is_for=is_for
    
    async def add_notification(self,notify_title:str,notify_body:str,notify_img_url:str|None=None,notify_id:Optional[str]=None):
        try:
            # ctx = self.session.begin() if not self.session.in_transaction() else nullcontext()
            async with maybe_begin(session=self.session):
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
        
    async def update_add_notify_reciv_user(self,user:Users):
        try:
            async with self.session.begin():
                notify_recvd_user_query=await self.session.execute(select(NotificationRecivedUsers).where(NotificationRecivedUsers.user_id==user.id))
                notify_recvd_user=notify_recvd_user_query.scalar_one_or_none()
                utc_now=datetime.now(timezone.utc)

                if notify_recvd_user:
                    notify_recvd_user.last_checked=utc_now
                else:
                    notify_user_to_add=NotificationRecivedUsers(
                        user_id=user.id,
                        last_checked=utc_now
                    )
                    self.session.add(
                        notify_user_to_add
                    )
                ic("notification seen updated successfully")

        except Exception as e:
            ic(f"something went wrong while updating notification seen {e}")
    
    async def get_notifications(self):
        try:
            user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
            async def get_seen_notifications(last_checked):
                ic("seen notification called")
                notifications=await self.session.execute(
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
                )
                return notifications.mappings().all()
            
            async def get_new_notifications(last_checked):
                ic("new notification called")
                notifications=await self.session.execute(
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
                )

                return notifications.mappings().all()
            
            async def get_all_notifications():
                ic("all notification called")
                notifications=await self.session.execute(
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
                )
                return notifications.mappings().all()

            
            last_checked_query=await self.session.execute(select(NotificationRecivedUsers.last_checked).where(NotificationRecivedUsers.user_id==user.id))
            last_checked=last_checked_query.scalar()
            ic(last_checked)
            if not last_checked:
                tasks=[get_all_notifications()]
            else:
                tasks=[get_new_notifications(last_checked),get_seen_notifications(last_checked)]

            compeleted_tasks=await asyncio.gather(*tasks)

            notifications={"notifications":{"new":compeleted_tasks[0],"seen":[]}}
            if len(compeleted_tasks)==2:
                notifications['notifications']["seen"]=compeleted_tasks[1]
            return notifications
        
        except HTTPException:
            raise

        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while fetching notifications {e}"
            )