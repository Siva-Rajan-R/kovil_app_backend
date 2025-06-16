from fastapi import FastAPI,middleware
from fastapi.responses import ORJSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from brotli_asgi import BrotliMiddleware
from api.routes import dashboard, event_crud, user_auth ,event_info,user_crud,panchagam_calendar,workers_crud,app_version
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from contextlib import asynccontextmanager
from database.operations.notification import delete_expired_notification
import os
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

# middlewares

app.add_middleware(GZipMiddleware,minimum_size=400,compresslevel=9)