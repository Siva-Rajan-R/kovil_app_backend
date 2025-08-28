from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

Engine=create_async_engine(DATABASE_URL,pool_size=5,max_overflow=10,pool_pre_ping=True,pool_recycle=1200,)

Base=declarative_base()

SessionLocal=async_sessionmaker(Engine)

async def get_db_session():
    session=SessionLocal()
    try:
        yield session
    finally:
        await session.close()

from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db_session_ctx():
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
