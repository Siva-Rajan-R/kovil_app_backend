from database.models.user import Users
from enums import backend_enums
from sqlalchemy import exists,or_,select,update
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from fastapi import HTTPException,BackgroundTasks
from security.hashing import hash_data,verify_hash
from security.jwt_token import JwtTokenCreation
from security.uuid_creation import create_unique_id
from datetime import datetime,timedelta,timezone
from firebase_db.operations import FirebaseCrud
import os
from icecream import ic

JWT_TOKEN_EXPIRY_IN_DAYS=int(os.getenv("JWT_TOKEN_EXPIRY_IN_DAYS"))


class __UserRegisterationInputs:
    def __init__(self,session:AsyncSession,name:str,mobile_number:str,email:EmailStr,role:backend_enums.UserRole,password:str):
        self.session=session
        self.name=name
        self.mobile_number=mobile_number
        self.email=email
        self.role=role
        self.password=password

class __UserLoginInputs:
    def __init__(self,session:AsyncSession,email_or_no:str|EmailStr,password:str):
        self.session=session
        self.email_or_no=email_or_no
        self.password=password

class __UserForgotInputs:
    def __init__(self,session:AsyncSession,email_or_no:str|EmailStr,new_password:str):
        self.session=session
        self.email_or_no=email_or_no
        self.new_password=new_password


class UserVerification:
    def __init__(self,session:AsyncSession):
        self.session=session

    async def is_user_not_exists(self,email:EmailStr,mobile_number:str):
        user_id=await self.session.execute(select(Users.id).where(or_(Users.email==email,Users.mobile_number==mobile_number)))
        if not user_id.scalar_one_or_none():
            return True
        raise HTTPException(status_code=409,detail="user already exists")
    
    async def is_user_exists(self,email_or_no:EmailStr|str):
       user_query=await self.session.execute(select(Users).where(or_(Users.email==email_or_no,Users.mobile_number==email_or_no)))
       user=user_query.scalar_one_or_none()
       if user:
           return user
       raise HTTPException(status_code=404,detail="user doesn't exists")
    
    async def is_user_exists_by_id(self,id:str):
       user_query=await self.session.execute(select(Users).where(Users.id==id))
       user=user_query.scalar_one_or_none()
       if user:
           return user
       raise HTTPException(status_code=404,detail="user doesn't exists")
    
class UserRegisteration(__UserRegisterationInputs):
    async def register(self):
        try:
            async with self.session.begin():
                await UserVerification(self.session).is_user_not_exists(email=self.email,mobile_number=self.mobile_number)
                user_id=await create_unique_id(self.email)
                user=Users(
                    id=user_id,
                    name=self.name,
                    mobile_number=self.mobile_number,
                    email=self.email,
                    role=self.role,
                    password=await hash_data(self.password),
                    created_at=datetime.now(timezone.utc)
                )

                self.session.add(user)
                return "user registered successfully"
        
        except HTTPException:
            raise

        except Exception as e:
            ic(f"something went wrong while register user {e}")
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while register user {e}"
            )

class UserLogin(__UserLoginInputs):
    
    async def login(self,data):
        try:
            user=await UserVerification(session=self.session).is_user_exists(email_or_no=self.email_or_no)
            is_verified=await verify_hash(hashed_data=user.password,plain_data=self.password)
            if is_verified:
                data["id"]=user.id
                user_role=user.role.name
                print(user_role)

                jwt_token=JwtTokenCreation(
                    data=data
                )

                return {
                    "access_token":await jwt_token.access_token(),
                    "refresh_token":await jwt_token.refresh_token(),
                    "role":user_role,
                    "refresh_token_exp_date":str((datetime.now()+timedelta(days=JWT_TOKEN_EXPIRY_IN_DAYS)).date())
                }
            else:
                raise HTTPException(
                    status_code=422,
                    detail="invalid email,number, or password".title()
                )
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while login {e}"
            )
        
class UserForgot(__UserForgotInputs):

    async def update_user_password(self):
        try:
            async with self.session.begin():
                user_update_query=update(Users).where(
                    or_(Users.email==self.email_or_no,Users.mobile_number==self.email_or_no)
                ).values(
                    password=await hash_data(data=self.new_password)
                )
                await self.session.execute(user_update_query)
                    
                return "Successfully password updated"
        
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while updating password {e}"
            )
