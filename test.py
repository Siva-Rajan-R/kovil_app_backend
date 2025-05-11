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

for i in zip([1,2,3,45],[1,6,8,9]):
    print(i[0],i[1])

print(dict(zip([1,2,3,45],[1,6,8,9])))


query_to_update=self.session.query(Workers).filter(Workers.name==workername[1])
                    ic(workername[1])
                    if query_to_update.one_or_none():
                        partic_log=self.session.query(WorkersParticipationLogs.worker_id).filter(WorkersParticipationLogs.event_id==self.event_id,WorkersParticipationLogs.worker_id==query_to_update.one_or_none().id).all()
                        if len(partic_log)!=len(previous_names):
                            ic(query_to_update.one_or_none().no_of_participated_events)
                            query_to_update.update(
                                {
                                    Workers.no_of_participated_events:query_to_update.one_or_none().no_of_participated_events+1
                                }
                            )
                            
                            print("hello")
                            add_wrk_parti_logs.append(
                                WorkersParticipationLogs(
                                    event_id=self.event_id,
                                    worker_id=query_to_update.one_or_none().id
                                )
                            )
                            
                            wk_name=self.session.query(workername[0]).filter(EventsStatus.event_id==self.event_id).scalar()
                            q_to_up=self.session.query(Workers).filter(Workers.name==wk_name)
                            ic(wk_name,q_to_up.one_or_none())
                            if q_to_up.one_or_none():
                                q_to_up.update(
                                    {
                                        Workers.no_of_participated_events:q_to_up.one_or_none().no_of_participated_events-1
                                    }
                                )

                            temp_log.append(workername[1])

                            ic(add_wrk_parti_logs)

                    else:
                        raise HTTPException(
                            status_code=404,
                            detail="Invalid worker names"
                        )