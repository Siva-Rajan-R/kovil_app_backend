from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from database.main import Base,Engine



class Workers(Base):
    __tablename__="workers"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String,nullable=False,unique=True)
    mobile_number=Column(String,nullable=False,unique=True)
    no_of_participated_events=Column(Integer,nullable=False,default=0)

    wrk_partic_log=relationship("WorkersParticipationLogs",back_populates="worker",cascade="all, delete-orphan")

class WorkersParticipationLogs(Base):
    __tablename__="workers_participation_logs"
    id=Column(Integer,primary_key=True,autoincrement=True)
    event_id=Column(String,nullable=False)
    worker_id=Column(Integer,ForeignKey("workers.id",ondelete="CASCADE"))

    worker=relationship("Workers",back_populates="wrk_partic_log")

Base.metadata.create_all(Engine)