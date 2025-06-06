from firebase_db.operations import FirebaseCrud
from pyfcm import FCMNotification
from fastapi.exceptions import HTTPException


class PushNotificationCrud:
    def __init__(self,notify_title:str,notify_body:str,data_payload:dict):
        self.fcm_init=FCMNotification(
            service_account_file="nanmaitharvuar-kovilapp-firebase-adminsdk-fbsvc-6ab7a4b1a6.json",
            project_id="nanmaitharvuar-kovilapp"
        )
        self.notify_title=notify_title
        self.notify_body=notify_body
        self.data_payload=data_payload

    async def push_notifications_individually(self,fcm_tokens:list):
        try:
            print(fcm_tokens)
            for token in fcm_tokens:
                print("hello")
                self.fcm_init.notify(
                    fcm_token=token,
                    notification_title=self.notify_title,
                    notification_body=self.notify_body,
                    data_payload=self.data_payload
                )

                print("...suuccesss notify...")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong {e}"
            )
            
