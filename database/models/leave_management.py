from sqlalchemy import Column,Integer,String,ForeignKey,Date,Time,Enum,LargeBinary,Boolean,DateTime
from sqlalchemy.orm import relationship
from database.main import Base,Engine
from enums import backend_enums
from datetime import datetime


class LeaveManagement(Base):
    __tablename__="leave_management"
    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(String,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    from_date=Column(Date,nullable=False)
    to_date=Column(Date,nullable=False)
    reason=Column(String,nullable=False)
    status=Column(Enum(backend_enums.LeaveStatus),default=backend_enums.LeaveStatus.WAITING)
    datetime=Column(DateTime(timezone=True))

    user=relationship("Users",back_populates="leave_management")


Base.metadata.create_all(Engine)
