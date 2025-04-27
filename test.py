from datetime import datetime,timezone,timedelta
print(datetime.now(timezone.utc)+timedelta(days=7))