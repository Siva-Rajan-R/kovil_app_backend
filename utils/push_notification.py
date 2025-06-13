from firebase_db.operations import FirebaseCrud
from fastapi.exceptions import HTTPException
import os,json
from firebase_admin import messaging, credentials, initialize_app
from typing import List,OrderedDict,Optional
from dotenv import load_dotenv
from icecream import ic
load_dotenv()

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
    def __init__(self,notify_title:str,notify_body:str,data_payload:dict):
        
        self.notify_title=notify_title
        self.notify_body=notify_body
        self.data_payload=data_payload

    def push_notifications_individually(self,fcm_tokens:list|OrderedDict,unsubscribe:Optional[bool]=False,remove_in_db:Optional[bool]=False,user_id:Optional[str]=None,image_url:Optional[str]=None):
        print(fcm_tokens)
        
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


    def push_notifications_individually_by_tokens(self,fcm_tokens:list,image_url:Optional[str]=None):
        print(fcm_tokens)
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

                response=messaging.send(message=message)
                print(f"...suuccesss notify... {response}")

            except Exception as e:
                ic("notification fail")
        
    def push_notification_to_all(self,image_url:Optional[str]=None):
        message=messaging.Message(
                notification=messaging.Notification(
                    title=self.notify_title,
                    body=self.notify_body,
                    image=image_url
                ),
                data=self.data_payload,
                topic="all"
            )
        response=messaging.send(message=message)
        print(f"...suuccesss notify... {response}")
            
