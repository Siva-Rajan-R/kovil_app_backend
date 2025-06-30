from redis.asyncio import Redis
from dotenv import load_dotenv
load_dotenv()
import os

redis_url=os.getenv("REDIS_URL")
redis=Redis.from_url(
    url=redis_url,
    decode_responses=True,
    max_connections=25
)