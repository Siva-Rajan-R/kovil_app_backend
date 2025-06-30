from utils.push_notification import PushNotificationCrud
from firebase_db.operations import FirebaseCrud
from typing import Any
from icecream import ic


async def send_error_notification(user_id:str,error_title:str,error_body:str,notify_data_payload:dict):

    user_fcm_tokens=FirebaseCrud(user_id=user_id).get_fcm_tokens()
    await PushNotificationCrud(
        notify_title=error_title,
        notify_body=error_body,
        data_payload=notify_data_payload
    ).push_notifications_individually(fcm_tokens=user_fcm_tokens)

    ic("error notifications sended successfully")
