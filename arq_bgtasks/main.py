from arq.connections import RedisSettings
from arq_bgtasks.tasks import worker_report,events_to_email,event_completed_status,event_pending_canceled_status
from dotenv import load_dotenv
import os
load_dotenv

redis=os.getenv("REDIS_URL")

class WorkerSettings:
    redis_settings=RedisSettings.from_dsn(redis)
    connection_pool_kwargs={
            "socket_connect_timeout": 60,  # seconds to wait for connection
            "socket_timeout": 60,          # seconds for read/write operations
        }
    functions=[worker_report,events_to_email,event_completed_status,event_pending_canceled_status]