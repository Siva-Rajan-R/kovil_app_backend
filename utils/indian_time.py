from datetime import datetime
import pytz

async def get_india_time():
    india_timezone = pytz.timezone('Asia/Kolkata')
    india_time = datetime.now(india_timezone).strftime("%I:%M %p")
    return india_time
