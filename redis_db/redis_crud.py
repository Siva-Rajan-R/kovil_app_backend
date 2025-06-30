from redis_db.main import redis
from fastapi.requests import Request
from icecream import ic
from typing import Optional


class RedisCrud:

    def __init__(self,key:str,expiry:Optional[int]=3600):
        self.key=key
        self.expity=expiry

    async def store_etag_to_redis(self,etag:str):
        await redis.set(name=self.key,value=etag,ex=self.expity)

        ic("succefully stored")

    async def unlink_etag_from_redis(self,*keys):
        ic(*keys)
        await redis.unlink(*keys if keys else [self.key])

        ic("unliked succefully")

    async def get_etag_from_redis(self):
        return await redis.get(self.key)