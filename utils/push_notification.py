from firebase_db.operations import FirebaseCrud
from fastapi.exceptions import HTTPException
import os,json
from firebase_admin import messaging, credentials, initialize_app
from typing import List,OrderedDict,Optional
from dotenv import load_dotenv
from icecream import ic
import time
load_dotenv()
from redis_db.redis_crud import RedisCrud
from redis_db.redis_etag_keys import NOTIFICATION_ETAG_KEY

fcm_cred=os.getenv("FCM_CREDENTIAL")

if not fcm_cred:
    raise RuntimeError("Missing FIREBASE_SERVICE_ACCOUNT_JSON environment variable")

cred_dict = json.loads(fcm_cred)

try:
    cred = credentials.Certificate(cred_dict)
    default_app = initialize_app(cred)
except ValueError:
    raise

class PushNotificationCrud:
    def __init__(self,notify_title:str,notify_body:str,data_payload:dict,max_retries:int=3,delay=5):
        
        self.notify_title=notify_title
        self.notify_body=notify_body
        self.data_payload=data_payload
        self.max_retries=max_retries
        self.delay=delay
    
    async def _retry_send_notification(self,message):
        delay=self.delay
        for attempt in range(self.max_retries+1):
            try:
                response=messaging.send(message=message)
                print(f"...suuccesss notify... {response}")
                return
            except Exception as e:
                ic (f"something went wrong while sending notification {e}")

            if attempt<self.max_retries:
                time.sleep(delay)
                delay*=2
        ic("hello hiii")
        
        return None

    async def push_notifications_individually(self,fcm_tokens:list|OrderedDict,unsubscribe:Optional[bool]=False,remove_in_db:Optional[bool]=False,user_id:Optional[str]=None,image_url:Optional[str]=None):
        print(fcm_tokens)
        await RedisCrud(key=NOTIFICATION_ETAG_KEY).unlink_etag_from_redis()
        for device_id,token in fcm_tokens.items():
            print(device_id)
            print("vanakam pangali")
            try:
                if unsubscribe:
                    messaging.unsubscribe_from_topic(tokens=[token],topic="all")
            
                message=messaging.Message(
                    notification=messaging.Notification(
                        title=self.notify_title,
                        body=self.notify_body,
                        image=image_url
                    ),
                    token=token,
                    data=self.data_payload
                )

                if remove_in_db:
                    res=FirebaseCrud(user_id=user_id).delete_fcm_token(device_id=device_id)
                    ic(res)

                response=messaging.send(message=message)
                print(f"...suuccesss notify... {response}")

            except Exception as e:
                ic(f"error notification {e}")
                res=FirebaseCrud(user_id=user_id).delete_fcm_token(device_id=device_id)
                ic(res)


    async def push_notifications_individually_by_tokens(self,fcm_tokens:list,image_url:Optional[str]=None):
        print(fcm_tokens)
        await RedisCrud(key=NOTIFICATION_ETAG_KEY).unlink_etag_from_redis()
        for token in fcm_tokens:
            print(token)
            try:
                message=messaging.Message(
                    notification=messaging.Notification(
                        title=self.notify_title,
                        body=self.notify_body,
                        image=image_url
                    ),
                    token=token,
                    data=self.data_payload
                )

                response=await self._retry_send_notification(message=message)
                print(f"...suuccesss notify... {response}")

            except Exception as e:
                ic("notification fail")
        
    async def push_notification_to_all(self,image_url:Optional[str]=None):
        await RedisCrud(key=NOTIFICATION_ETAG_KEY).unlink_etag_from_redis()
        message=messaging.Message(
                notification=messaging.Notification(
                    title=self.notify_title,
                    body=self.notify_body,
                    image=image_url
                ),
                data=self.data_payload,
                topic="hii"
            )
        response=await self._retry_send_notification(message=message)
        print(f"...suuccesss notify... {response}")
