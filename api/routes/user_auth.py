from fastapi import APIRouter,Request,Depends,BackgroundTasks,Response,HTTPException
from fastapi.responses import ORJSONResponse
from database.operations.user_auth import UserRegisteration,UserLogin,UserVerification,UserForgot
from database.main import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas import user_auth
from api.dependencies import token_revocation,email_automation
from templates.pyhtml import report
from security.uuid_creation import create_unique_id
from security.hashing import hash_data,verify_hash
from firebase_db.operations import FirebaseCrud
from utils.push_notification import PushNotificationCrud
from icecream import ic
import asyncio
from redis_db.redis_crud import RedisCrud
from redis_db.redis_etag_keys import USER_ETAG_KEY
router=APIRouter(
    tags=["Register,Login,forgot and delete Users"]
)

registeration_waiting_list={}
forgot_password_waiting_list={}

@router.post("/register")
async def register(request:Request,bgt:BackgroundTasks,register_inputs:user_auth.UserRegisterSchema,session:AsyncSession=Depends(get_db_session)):
    await UserVerification(
        session=session
    ).is_user_not_exists(email=register_inputs.email,mobile_number=register_inputs.mobile_number)

    link_id=await create_unique_id(register_inputs.name)

    registeration_waiting_list[link_id]=register_inputs
    bgt.add_task(email_automation.accept_or_forgot_email,
        email_subject="registeration accept request",
        name=register_inputs.name,
        email=register_inputs.email,
        number=register_inputs.mobile_number,
        role=register_inputs.role,
        href=f"{request.base_url}register/accept/{link_id}",
        isforgot=False
    )
    return ORJSONResponse(
        status_code=201,
        content=f"registered successfully waiting for admin conformation"
    )

@router.get("/register/accept/{link_id}")
async def register_accept(link_id:str,bgt:BackgroundTasks,session:AsyncSession=Depends(get_db_session)):
    registered_user_data=registeration_waiting_list.get(link_id,0)
    if registered_user_data:
        await UserRegisteration(
            session=session,
            name=registered_user_data.name,
            email=registered_user_data.email,
            mobile_number=registered_user_data.mobile_number,
            role=registered_user_data.role,
            password=registered_user_data.password
        ).register()

        del registeration_waiting_list[link_id]
        bgt.add_task(
            email_automation.register_or_forgot_successfull_email,
            email_subject="Your Registeration Accepted Successfully",
            email_body=f"Hi,{registered_user_data.name} Your registeration was confirmed by admin as a role of {registered_user_data.role} by nanmai tharuvar kovil",
            email=registered_user_data.email
        )
        ic(registered_user_data.fcm_token)
        if registered_user_data.fcm_token:
            asyncio.create_task(
                PushNotificationCrud(
                    notify_title="Registeration Successfull",
                    notify_body=f"Hi,{registered_user_data.name.title()} your Registeration Successfully Approved By Admin",
                    data_payload={
                        "screen":"login_page"
                    }
                ).push_notifications_individually_by_tokens(fcm_tokens=[registered_user_data.fcm_token])
                
            )
        await RedisCrud(key=USER_ETAG_KEY).unlink_etag_from_redis()
        return Response(
            content=report.register_accept_greet(registered_user_data.name,registered_user_data.email,registered_user_data.mobile_number,registered_user_data.role),
            media_type="text/html",
            status_code=200
        )
    return Response(
        content=report.not_found(),
        status_code=404,
        media_type="text/html"
    )

@router.post("/login")
async def login(request:Request,bgt:BackgroundTasks,login_inputs:user_auth.UserLoginSchema,session:AsyncSession=Depends(get_db_session)):
    data={
        "user_agent":request.headers.get("User-Agent"),
        "accept_language":request.headers.get("Accept-Language")
    }

    user_login=await UserLogin(
        session=session,
        email_or_no=login_inputs.email_or_no,
        password=login_inputs.password,
    ).login(data=data)

    return ORJSONResponse(
        status_code=200,
        content=user_login
    )

@router.put("/forgot")
async def forgot(request:Request,forgot_inputs:user_auth.UserForgotSchema,bgt:BackgroundTasks,session:AsyncSession=Depends(get_db_session)):
    user=await UserVerification(session=session).is_user_exists(email_or_no=forgot_inputs.email_or_no)
    link_id=await create_unique_id(forgot_inputs.email_or_no)
    is_exists=await verify_hash(user.password,forgot_inputs.new_password)
    ic(is_exists)
    if is_exists==False:
        forgot_inputs.new_password=forgot_inputs.new_password
        forgot_password_waiting_list[link_id]=forgot_inputs
        ic(user.email)
        ic(forgot_inputs.email_or_no)
        bgt.add_task(email_automation.accept_or_forgot_email,
            email_subject="new password accept request",
            name=user.name,
            email=user.email,
            number=user.mobile_number,
            href=f"{request.base_url}forgot/accept/{link_id}",
            isforgot=True,
            role=user.role
        )
        return ORJSONResponse(
            status_code=200,
            content="new password changed successfully waiting for your conformation"
        )
    raise HTTPException(
        status_code=409,
        detail="The given password is already exists"
    )


@router.get("/forgot/accept/{link_id}")
async def forgot_accept(link_id:str,bgt:BackgroundTasks,session:AsyncSession=Depends(get_db_session)):
    forgot_password_user_data=forgot_password_waiting_list.get(link_id,0)
    if forgot_password_user_data:
        await UserForgot(
            session=session,
            email_or_no=forgot_password_user_data.email_or_no,
            new_password=forgot_password_user_data.new_password
        ).update_user_password()
        del forgot_password_waiting_list[link_id]
        bgt.add_task(
            email_automation.register_or_forgot_successfull_email,
            email_subject="New password changed Successfully",
            email_body=f"Hi,{forgot_password_user_data.email_or_no} Your Password Was Changed Now By You for nanmai tharuvar kovil app!",
            email=forgot_password_user_data.email_or_no
        )

        if forgot_password_user_data.fcm_token:
            asyncio.create_task(
                PushNotificationCrud(
                    notify_title="Forgot Password",
                    notify_body=f"Password Changed Successfully For {forgot_password_user_data.email_or_no}",
                    data_payload={
                        "screen":"login_page"
                    }
                ).push_notifications_individually_by_tokens(fcm_tokens=[forgot_password_user_data.fcm_token])
                
            )
        
        return Response(
            content=report.forgot_accept_greet(forgot_password_user_data.email_or_no),
            media_type="text/html",
            status_code=200
        )
    return Response(
        content=report.not_found(),
        status_code=404,
        media_type="text/html"
    )


@router.get("/new-access-token")
def get_new_access_token(new_access_token:dict=Depends(token_revocation.revoke)):
    return ORJSONResponse(
        status_code=200,
        content=new_access_token
    )

