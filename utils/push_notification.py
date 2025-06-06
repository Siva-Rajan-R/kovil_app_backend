from firebase_db.operations import FirebaseCrud
from fastapi.exceptions import HTTPException
import os,json
from firebase_admin import messaging, credentials, initialize_app
from typing import List,OrderedDict
from dotenv import load_dotenv
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

    async def push_notifications_individually(self,fcm_tokens:list|OrderedDict):
        try:
            print(fcm_tokens)
            for device_id,token in fcm_tokens.items():
                print(device_id)
                message=messaging.Message(
                    notification=messaging.Notification(
                        title=self.notify_title,
                        body=self.notify_body,
                    ),
                    token=token,
                    data=self.data_payload
                )

                response=messaging.send(message=message)
                print(f"...suuccesss notify... {response}")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong {e}"
            )
    async def push_notifications_individually_by_tokens(self,fcm_tokens:list):
        try:
            print(fcm_tokens)
            for token in fcm_tokens:
                print(token)
                message=messaging.Message(
                    notification=messaging.Notification(
                        title=self.notify_title,
                        body=self.notify_body,
                    ),
                    token=token,
                    data=self.data_payload
                )

                response=messaging.send(message=message)
                print(f"...suuccesss notify... {response}")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong {e}"
            )
            
