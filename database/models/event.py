from sqlalchemy import Column,Integer,String,ForeignKey,Date,Time,Enum
from sqlalchemy.orm import relationship
from database.main import Base,Engine
from enums import backend_enums

class Events(Base):
    __tablename__="events"
    id=Column(String,primary_key=True)
    name=Column(String,nullable=False)
    description=Column(String,nullable=False)
    date=Column(Date,nullable=False)
    start_at=Column(Time,nullable=False)
    end_at=Column(Time,nullable=False)

    client=relationship("Clients",back_populates="event",cascade="all, delete-orphan")
    payment=relationship("Payments",back_populates="event",cascade="all, delete-orphan")
    event_status=relationship("EventsStatus",back_populates="event",cascade="all, delete-orphan")

class Clients(Base):
    __tablename__="clients"
    id=Column(Integer,autoincrement=True,primary_key=True)
    name=Column(String,nullable=False)
    mobile_number=Column(String,nullable=False)
    email=Column(String,nullable=True)
    event_id=Column(String,ForeignKey("events.id",ondelete="CASCADE"),nullable=False)

    event=relationship("Events",back_populates="client")

class Payments(Base):
    __tablename__="payments"
    id=Column(Integer,autoincrement=True,primary_key=True)
    total_amount=Column(Integer,nullable=False)
    paid_amount=Column(Integer,nullable=False)
    status=Column(Enum(backend_enums.PaymetStatus),default=backend_enums.PaymetStatus.NOT_PAID,nullable=False)
    mode=Column(Enum(backend_enums.PaymentMode),default=backend_enums.PaymentMode.OFFLINE)
    event_id=Column(String,ForeignKey("events.id",ondelete="CASCADE"),nullable=False)

    event=relationship("Events",back_populates="payment")

class EventsStatus(Base):
    __tablename__="events_status"
    id=Column(Integer,autoincrement=True,primary_key=True)
    status=Column(Enum(backend_enums.EventStatus),default=backend_enums.EventStatus.PENDING)
    event_id=Column(String,ForeignKey("events.id",ondelete="CASCADE"),nullable=False,unique=True)
    added_by=Column(String,nullable=False)
    updated_by=Column(String,nullable=True)

    event=relationship("Events",back_populates="event_status")

Base.metadata.create_all(Engine)
