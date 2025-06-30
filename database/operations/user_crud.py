from database.models.user import Users,UserRole
from sqlalchemy import select,update,delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,BackgroundTasks
from database.operations.user_auth import UserVerification
from enums import backend_enums
from icecream import ic
from firebase_db.operations import FirebaseCrud
from utils.push_notification import PushNotificationCrud
import asyncio

class __UserDeleteInputs:
    def __init__(self,session:AsyncSession,user_id:str,del_user_id:str,bg_task:BackgroundTasks):
        self.session=session
        self.user_id=user_id
        self.del_user_id=del_user_id
        self.bg_task=bg_task

class DeleteUser(__UserDeleteInputs):
    async def delete_user(self):
        
        try:
            async with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                ic(user.role)
                if user.role==UserRole.ADMIN:
                    deleting_query=delete(Users).where(Users.id==self.del_user_id).returning(Users.name)
                    result=await self.session.execute(deleting_query)
                    deleted_username=result.scalar_one_or_none()

                    if deleted_username:
                        
                        ic(self.del_user_id)
                        fcm_tokens=FirebaseCrud(user_id=self.del_user_id).get_fcm_tokens()
                        
                        if fcm_tokens:
                            asyncio.create_task(
                                PushNotificationCrud(
                                    notify_title="No More Access",
                                    notify_body=f"Hi, {deleted_username} You Are Removed By The Admin So No More Access To This App",
                                    data_payload={
                                        "screen":"home_page"
                                    }
                                ).push_notifications_individually(
                                    fcm_tokens=fcm_tokens,
                                    unsubscribe=True,
                                    remove_in_db=True,
                                    user_id=self.del_user_id
                                )
                            )
                        
                        return "user deleted successfully"
                    
                    raise HTTPException(
                        status_code=404,
                        detail="user doesn't exists"
                    )
                raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to make any changes"
                )
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while deleting user {e}"
            )


class GetUsers:
    def __init__(self,session:AsyncSession,user_id:str):
        self.session=session
        self.user_id=user_id

    async def get_users(self):
        try:
            user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
            if user.role==UserRole.ADMIN:
                users=await self.session.execute(
                    select(
                        Users.id,
                        Users.name,
                        Users.email,
                        Users.mobile_number,
                        Users.role
                    )
                )
                return {"users":users.mappings().all()}
            raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to get this information"
                )
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while fetching users {e}"
            )
        
class UpdateUser:
    def __init__(self,session:AsyncSession,user_id:str,bg_task:BackgroundTasks):
        self.session=session
        self.user_id=user_id
        self.bg_task=bg_task

    async def update_user_role(self,user_id_to_update:str,role_to_update:backend_enums.UserRole):
        try:
            async with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    update_query=update(Users).where(Users.id==user_id_to_update).values(role=role_to_update).returning(Users.name)
                    result=await self.session.execute(update_query)

                    fcm_tokens=FirebaseCrud(user_id=user_id_to_update).get_fcm_tokens()
                        
                    if fcm_tokens:
                        asyncio.create_task(
                            PushNotificationCrud(
                                notify_title="Role Changed",
                                notify_body=f"Hi, {result.scalar_one_or_none().title()} Your Current Role Was Changed To {role_to_update.value.title()}. Please Re-Login!",
                                data_payload={
                                    "screen":"home_page"
                                }
                            ).push_notifications_individually(fcm_tokens=fcm_tokens)
                            
                        )

                    return "user role updated successfully"
                else:
                    raise HTTPException(
                        status_code=401,
                        detail="you are not allowed to make any changes"
                    )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while updating user role {e}"
            )