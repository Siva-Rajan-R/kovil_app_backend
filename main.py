from fastapi import FastAPI,middleware,Request
from fastapi.responses import ORJSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from brotli_asgi import BrotliMiddleware
from api.routes import dashboard, event_crud, user_auth ,event_info,user_crud,panchagam_calendar,workers_crud,app_version,leave_management,client_page
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from contextlib import asynccontextmanager
from database.operations.notification import delete_expired_notification
from database.main import Engine,Base
import os,time
from icecream import ic
from dotenv import load_dotenv
load_dotenv()

# jobstores={"default":SQLAlchemyJobStore(os.getenv("DATABASE_URL"))}
import sys
ic(sys)
if sys.platform != "win32":
    import uvloop, asyncio
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

scheduler = AsyncIOScheduler()
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ASGI lifespan.startup
    try:
        async with Engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        scheduler.add_job(delete_expired_notification, "interval", minutes=30,max_instances=4,id="delete_expired_notifications")
        scheduler.start()
        ic("🔄 Scheduler started.")
        yield  # Run app
    except Exception as e:
        ic(f"❌ Startup failed: {e}")
        raise
    finally:
        # ASGI lifespan.shutdown
        scheduler.shutdown()
        ic("🛑 Scheduler shutdown.")

app=FastAPI(lifespan=lifespan,default_response_class=ORJSONResponse)

app.include_router(user_auth.router)
app.include_router(user_crud.router)
app.include_router(event_crud.router)
app.include_router(event_info.router)
app.include_router(dashboard.router)
app.include_router(panchagam_calendar.router)
app.include_router(workers_crud.router)
app.include_router(app_version.router)
app.include_router(leave_management.router)
app.include_router(client_page.router)

# middlewares

app.add_middleware(GZipMiddleware,minimum_size=300,compresslevel=9)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)[:6]
    ic(f"Request: {request.method}:{request.url} took {process_time:.4f}s")
    return response

# uvicorn main:app --host localhost --ssl-keyfile localhost-key.pem --ssl-certfile localhost.pem --reload