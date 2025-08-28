from sqlalchemy import String,Integer,ForeignKey,Column,Enum,DateTime
from sqlalchemy.orm import relationship
from enums.backend_enums import UserRole
from database.main import Base,Engine
from datetime import datetime,timezone

class Users(Base):
    __tablename__="users"
    id=Column(String,primary_key=True,index=True)
    name=Column(String,nullable=False)
    mobile_number=Column(String,nullable=False)
    email=Column(String,nullable=False)
    role=Column(Enum(UserRole),default=UserRole.USER,nullable=False)
    password=Column(String,nullable=False)
    created_at=Column(DateTime(timezone=True))

    notify_recvd_user=relationship("NotificationRecivedUsers",back_populates="user",cascade="all, delete-orphan")
    worker=relationship("Workers",back_populates="user",cascade="all, delete-orphan")
    leave_management=relationship("LeaveManagement",back_populates="user",cascade="all, delete-orphan")

# Base.metadata.create_all(Engine)