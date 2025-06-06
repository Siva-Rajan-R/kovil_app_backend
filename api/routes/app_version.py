from fastapi import APIRouter,BackgroundTasks,Depends,Query
import os
import json
from utils.push_notification import PushNotificationCrud
from firebase_db.operations import FirebaseCrud
from api.schemas.application import NotifySchema,RegisterNotifySchema,DeleteNotifySchema
from database.operations.user_auth import UserVerification
from dotenv import load_dotenv
from database.main import get_db_session
from sqlalchemy.orm import Session
from icecream import ic
from api.dependencies.token_verification import verify
load_dotenv()


router=APIRouter(
    tags=["get the current version"]
)

version_info=os.getenv("VERSION_INFO")

@router.get("/app/version")
def get_app_version():
    return json.loads(version_info)

@router.post("/app/notify/all")
async def send_app_notify(notify_inputs:NotifySchema,bgt:BackgroundTasks):
    fcm_tokens=[
        {"device_id":"fUKAXNhpQHCOiuFfHT8PQ-:APA91bEYqkU1qtNyE5UDeqDyi1bgI9Rfmqm1bvg2u6IJm5wgngmCjW9M0LWibAdjfY6G6OrEO0qwLrFb9cI6tVN2NafT4h-KDn2gd_1a6BPgxiFn07nbrC4"}
    ]
    bgt.add_task(
        PushNotificationCrud(
            notify_title=notify_inputs.notification_title,
            notify_body=notify_inputs.notification_body,
            data_payload={
                "screen":"event_page"
            }
        ).push_notifications_individually,
        fcm_tokens=fcm_tokens
    )

    return "sended notification successfully"

@router.post("/app/notify/register-update")
async def register_fcm_token(register_inp:RegisterNotifySchema,bgt:BackgroundTasks,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']
    if register_inp.user_email_or_no:
        user=await UserVerification(session=session).is_user_exists(email_or_no=register_inp.user_email_or_no)
        user_id=user.id
    bgt.add_task(
        FirebaseCrud(user_id=user_id).add_fcm_tokens,
        fcm_token=register_inp.fcm_token,
        device_id=register_inp.device_id
    )

    ic("added successfuly")

@router.delete("/app/notify/token")
async def delete_fcm_token(register_inp:DeleteNotifySchema,bgt:BackgroundTasks,session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user['id']

    bgt.add_task(
        FirebaseCrud(user_id=user_id).delete_fcm_token,
        device_id=register_inp.device_id
    )

    ic("successfully deleted")
