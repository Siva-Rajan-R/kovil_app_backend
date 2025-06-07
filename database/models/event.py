from sqlalchemy import Column,Integer,String,ForeignKey,Date,Time,Enum,LargeBinary,Boolean
from sqlalchemy.orm import relationship
from database.main import Base,Engine
from enums import backend_enums
from datetime import datetime

class EventNames(Base):
    __tablename__="event_names"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String,nullable=False)
    amount=Column(Integer,nullable=False)
    is_special=Column(Boolean,nullable=False)

class NeivethiyamNames(Base):
    __tablename__="neivethiyam_names"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String,nullable=False)
    amount=Column(Integer,nullable=False)
    

class Events(Base):
    __tablename__="events"
    id=Column(String,primary_key=True)
    name=Column(String,nullable=False)
    description=Column(String,nullable=False)
    status=Column(Enum(backend_enums.EventStatus),default=backend_enums.EventStatus.PENDING)
    added_by=Column(String,nullable=False)
    updated_by=Column(String,nullable=True)
    date=Column(Date,nullable=False)
    start_at=Column(String,nullable=False)
    end_at=Column(String,nullable=False)
    is_special=Column(Boolean,nullable=True)

    client=relationship("Clients",back_populates="event",cascade="all, delete-orphan")
    payment=relationship("Payments",back_populates="event",cascade="all, delete-orphan")
    event_completed_status=relationship("EventsCompletedStatus",back_populates="event",cascade="all, delete-orphan")
    event_pending_canceled_status=relationship("EventsPendingCanceledStatus",back_populates="event",cascade="all, delete-orphan")
    event_neivethiyam=relationship("EventsNeivethiyam",back_populates="event",cascade="all, delete-orphan")
    event_contact_desc=relationship("EventsContactDescription",back_populates="event",cascade="all, delete-orphan")
    worker_participation_log=relationship("WorkersParticipationLogs",back_populates="event",cascade="all, delete-orphan")
    
class EventsNeivethiyam(Base):
    __tablename__="events_neivethiyam"
    id=Column(Integer,primary_key=True,autoincrement=True)
    neivethiyam_id=Column(Integer,ForeignKey("neivethiyam_names.id"),nullable=False)
    event_id=Column(String,ForeignKey("events.id",ondelete="CASCADE"),nullable=False)
    padi_kg=Column(Integer,nullable=False)

    event=relationship("Events",back_populates="event_neivethiyam")

class Clients(Base):
    __tablename__="clients"
    id=Column(Integer,autoincrement=True,primary_key=True)
    name=Column(String,nullable=False)
    mobile_number=Column(String,nullable=False)
    city=Column(String,nullable=False)
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

class EventsCompletedStatus(Base):
    __tablename__="events_completed_status"
    id=Column(String,primary_key=True)
    event_id=Column(String,ForeignKey("events.id",ondelete="CASCADE"),nullable=False,unique=True)
    image_url=Column(String)
    feedback=Column(String)
    archagar=Column(String)
    abisegam=Column(String)
    helper=Column(String)
    poo=Column(String)
    read=Column(String)
    prepare=Column(String)
    updated_date=Column(Date,default=datetime.now().date())
    updated_at=Column(String)

    event_status_image=relationship("EventStatusImages",back_populates="event_completed_status",cascade="all, delete-orphan")
    event=relationship("Events",back_populates="event_completed_status")

class EventsPendingCanceledStatus(Base):
    __tablename__="events_pending_canceled_status"
    id=Column(Integer,autoincrement=True,primary_key=True)
    event_id=Column(String,ForeignKey("events.id",ondelete="CASCADE"),nullable=False,unique=True)
    description=Column(String)
    updated_date=Column(Date,default=datetime.now().date())
    updated_at=Column(String)

    event=relationship("Events",back_populates="event_pending_canceled_status")

class EventStatusImages(Base):
    __tablename__="event_status_images"
    id=Column(String,primary_key=True)
    image=Column(LargeBinary)
    event_sts_id=Column(String,ForeignKey("events_completed_status.id",ondelete="CASCADE"))

    event_completed_status=relationship("EventsCompletedStatus",back_populates="event_status_image")

class EventsContactDescription(Base):
    __tablename__="events_contact_description"
    id=Column(Integer,primary_key=True,autoincrement=True)
    description=Column(String,nullable=False)
    event_id=Column(String,ForeignKey("events.id",ondelete="CASCADE"),nullable=False)
    updated_by=Column(String,nullable=False)
    updated_at=Column(String,nullable=False)
    updated_date=Column(String,nullable=False)
    
    event=relationship("Events",back_populates="event_contact_desc")

Base.metadata.create_all(Engine)
