from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
@asynccontextmanager
async def maybe_begin(session:AsyncSession):
    if not session.in_transaction():
        async with session.begin():
            yield
    else:
        yield