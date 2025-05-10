from sqlalchemy import Column,Integer,String
from database.main import Base,Engine



class Workers(Base):
    __tablename__="workers"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String,nullable=False)
    mobile_number=Column(String,nullable=False,unique=True)
    no_of_participated_events=Column(Integer,nullable=False,default=0)

Base.metadata.create_all(Engine)