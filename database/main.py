from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

Engine=create_engine(DATABASE_URL)

Base=declarative_base()

SessionLocal=sessionmaker(Engine)

def get_db_session():
    session=SessionLocal()
    try:
        yield session
    finally:
        session.close()
