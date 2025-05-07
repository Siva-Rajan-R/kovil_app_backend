from sqlalchemy import Column,Integer,String,ForeignKey,Date,Time,Enum,LargeBinary
from sqlalchemy.orm import relationship
from database.main import Base,Engine
from enums import backend_enums
from datetime import datetime

class EventNames(Base):
    __tablename__="event_names"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String,nullable=False)
    amount=Column(Integer,nullable=False)

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
    date=Column(Date,nullable=False)
    start_at=Column(String,nullable=False)
    end_at=Column(String,nullable=False)

    client=relationship("Clients",back_populates="event",cascade="all, delete-orphan")
    payment=relationship("Payments",back_populates="event",cascade="all, delete-orphan")
    event_status=relationship("EventsStatus",back_populates="event",cascade="all, delete-orphan")

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

class EventsStatus(Base):
    __tablename__="events_status"
    id=Column(Integer,autoincrement=True,primary_key=True)
    status=Column(Enum(backend_enums.EventStatus),default=backend_enums.EventStatus.PENDING)
    event_id=Column(String,ForeignKey("events.id",ondelete="CASCADE"),nullable=False,unique=True)
    added_by=Column(String,nullable=False)
    updated_by=Column(String,nullable=True)
    image_url=Column(String)
    feedback=Column(String)
    tips=Column(String)
    poojai=Column(String)
    abisegam=Column(String)
    helper=Column(String)
    poo=Column(String)
    read=Column(String)
    prepare=Column(String)
    tips_shared=Column(String)
    tips_given_to=Column(String)
    updated_date=Column(Date,default=datetime.now().date())
    updated_at=Column(String)

    event_status_image=relationship("EventStatusImages",back_populates="event_status",cascade="all, delete-orphan")
    event=relationship("Events",back_populates="event_status")

class EventStatusImages(Base):
    __tablename__="event_status_images"
    id=Column(String,primary_key=True)
    image=Column(LargeBinary)
    event_sts_id=Column(Integer,ForeignKey("events_status.id",ondelete="CASCADE"))

    event_status=relationship("EventsStatus",back_populates="event_status_image")

Base.metadata.create_all(Engine)
