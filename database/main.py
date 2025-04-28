from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

Engine=create_engine(DATABASE_URL)

Base=declarative_base()

def get_db_session():
    Session=sessionmaker(Engine)
    session=Session()
    try:
        yield session
    finally:
        session.close()
