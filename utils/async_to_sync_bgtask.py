import asyncio

def run_async_in_bg(func, *args, **kwargs):
    def wrapper():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(func(*args, **kwargs))
        loop.close()
    return wrapper

