from fastapi import FastAPI,middleware,Request
from fastapi.responses import ORJSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from brotli_asgi import BrotliMiddleware
from api.routes import dashboard, event_crud, user_auth ,event_info,user_crud,panchagam_calendar,workers_crud,app_version,leave_management
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from contextlib import asynccontextmanager
from database.operations.notification import delete_expired_notification
import os,time
from icecream import ic
from dotenv import load_dotenv
load_dotenv()

# jobstores={"default":SQLAlchemyJobStore(os.getenv("DATABASE_URL"))}

scheduler = BackgroundScheduler()
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ASGI lifespan.startup
    try:
        scheduler.add_job(delete_expired_notification, "interval", minutes=30,max_instances=4)
        scheduler.start()
        print("🔄 Scheduler started.")
        yield  # Run app
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        raise
    finally:
        # ASGI lifespan.shutdown
        scheduler.shutdown()
        print("🛑 Scheduler shutdown.")

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

# middlewares

app.add_middleware(GZipMiddleware,minimum_size=300,compresslevel=9)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)[:6]
    ic(f"Request: {request.url} took {process_time:.4f}s")
    return response

# uvicorn main:app --host localhost --ssl-keyfile localhost-key.pem --ssl-certfile localhost.pem --reload