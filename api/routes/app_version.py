from fastapi import APIRouter
import os
import json
from utils.push_notification import PushNotificationCrud
from api.schemas.application import NotifySchema
from dotenv import load_dotenv
load_dotenv()


router=APIRouter(
    tags=["get the current version"]
)

version_info=os.getenv("VERSION_INFO")

@router.get("/app/version")
def get_app_version():
    return json.loads(version_info)

@router.post("/app/notify")
async def get_app_notify(notify_inputs:NotifySchema):
    fcm_tokens=[
        "fUKAXNhpQHCOiuFfHT8PQ-:APA91bEYqkU1qtNyE5UDeqDyi1bgI9Rfmqm1bvg2u6IJm5wgngmCjW9M0LWibAdjfY6G6OrEO0qwLrFb9cI6tVN2NafT4h-KDn2gd_1a6BPgxiFn07nbrC4"
    ]
    await PushNotificationCrud(
        notify_title=notify_inputs.notification_title,
        notify_body=notify_inputs.notification_body,
        data_payload={
            "screen":"event_page"
        }
    ).push_notifications_individually(fcm_tokens=fcm_tokens)

    return "sended notification successfully"