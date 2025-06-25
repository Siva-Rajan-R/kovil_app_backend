from sqlalchemy import Column,Integer,String,ForeignKey,Date,Time,Enum,LargeBinary,Boolean,DateTime
from sqlalchemy.orm import relationship
from database.main import Base,Engine
from enums import backend_enums
from datetime import datetime,timezone

class Notifications(Base):
    __tablename__="notifications"
    id=Column(String,primary_key=True)
    title=Column(String,nullable=False)
    body=Column(String,nullable=False)
    image_url=Column(String,nullable=True)
    is_for=Column(String,nullable=False)
    created_by=Column(String,nullable=False)
    created_at=Column(DateTime(timezone=True),nullable=False)

    notify_image=relationship("NotificationImages",back_populates="notify",cascade="all, delete-orphan")

class NotificationImages(Base):
    __tablename__="notification_images"
    id=Column(String,primary_key=True)
    image=Column(LargeBinary,nullable=False)
    notify_id=Column(String,ForeignKey("notifications.id",ondelete="CASCADE"))
    created_at=Column(DateTime(timezone=True),nullable=False)

    notify=relationship("Notifications",back_populates="notify_image")

class NotificationRecivedUsers(Base):
    __tablename__="notification_recived_users"
    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(String,ForeignKey("users.id",ondelete="CASCADE"))
    last_checked=Column(DateTime(timezone=True),nullable=False)

    user=relationship("Users",back_populates="notify_recvd_user")


Base.metadata.create_all(Engine)