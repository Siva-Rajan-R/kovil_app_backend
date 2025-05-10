# from datetime import datetime

# updated_at = datetime.now().strftime("%I:%M %p")
# print(updated_at)


# from datetime import datetime
# import pytz

# india_timezone = pytz.timezone('Asia/Kolkata')
# updated_at = datetime.now(india_timezone).strftime("%I:%M:%S %p")
# print(updated_at)


# import requests

# head={
#     "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDU5OTY0MjYsImRhdGEiOiJnQUFBQUFCb0VjY0dvR2JIcWNYQnBnUGFnVnpTSjdkQ2RZaHpHS1QtWEtDRnlaSnZMNjZEMFFZRG1QcjZTOERjLTVrQjJEbkdVSklzRjMyWVRLeTFYdHFPN1I3T19FdWZBU3JTdjhOUWZBZnJ3Rk9lZTBKLUgwTTcxN21MeEdVaXgxcVgwVGJvVkVSTFc3V0pSaFdvQ2JiREdvZVp2UVhQTlRkeVRnbmNwMmhxRzNfVmhZcFNRX19HWVpnbUFkMGhlTzFsSTlSUWdveUFfams0MkJOaWQtTjJxVVZfQzVUc1Z3PT0ifQ.V7fbzoZFusJbgDoZZiPjcSPuvbIGtk21JlZgDl_D3OU"
# }
# # res=requests.post("http://127.0.0.1:8000/event/name",json={"event_name":None,"event_amount":0},headers=head)

# # # res=requests.post("http://127.0.0.1:8000/login",json={"email_or_no":'string',"password":'string'})

# # # print(res.content)
# # # from enum import Enum
# # # class EventStatus(Enum):
# # #     COMPLETED="completed"
# # #     PENDING="pending"
# # #     CANCELED="canceled"

# # # print([i.value for i in EventStatus])

# # print(4000<3000)


import re

def clean_phone_numbers(input_string):
    # Find all digit sequences and join them with a hyphen
    numbers = re.findall(r'\d+', input_string)
    print(numbers)
    return '-'.join(numbers)

# Example usage
input_string = "1234567890-1234567890,1234567890 1234567890"
cleaned = clean_phone_numbers(input_string)
print("Cleaned phone numbers:", cleaned)
a=[(1,2,3,4),(1,2)]
print(list(a))
b=[1,2,3,4,5]
if b == [1,2,3,4,5,6]:
    print(True)
else:
    print(False)
