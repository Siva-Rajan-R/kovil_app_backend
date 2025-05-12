from sqlalchemy import Column, Integer, String, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from database.main import Base, Engine

class Workers(Base):
    __tablename__ = "workers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    mobile_number = Column(String, nullable=False, unique=True)

    wrk_partic_log = relationship("WorkersParticipationLogs", back_populates="worker", cascade="all, delete-orphan")

class WorkersParticipationLogs(Base):
    __tablename__ = "workers_participation_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    worker_id = Column(Integer, ForeignKey("workers.id", ondelete="CASCADE"), nullable=False)
    no_of_participation = Column(Integer)
    is_reseted=Column(Boolean,default=False)

    worker = relationship("Workers", back_populates="wrk_partic_log")
    event = relationship("Events",back_populates="worker_participation_log")

Base.metadata.create_all(Engine)
