from sqlalchemy import Column,Integer,String,ForeignKey,Date,Time,Enum,LargeBinary,Boolean
from sqlalchemy.orm import relationship
from database.main import Base,Engine
from enums import backend_enums
from datetime import datetime

class NotificationImages(Base):
    __tablename__="notification_images"
    id=Column(String,primary_key=True)
    image=Column(LargeBinary,nullable=False)


Base.metadata.create_all(Engine)