from datetime import datetime

updated_at = datetime.now().strftime("%I:%M %p")
print(updated_at)


from datetime import datetime
import pytz

india_timezone = pytz.timezone('Asia/Kolkata')
updated_at = datetime.now(india_timezone).strftime("%I:%M:%S %p")
print(updated_at)
