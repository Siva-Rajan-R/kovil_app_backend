from database.models.user import Users,UserRole
from sqlalchemy import select,exists,or_
from sqlalchemy.orm import Session
from pydantic import EmailStr
from fastapi.exceptions import HTTPException
import uuid
from security.hashing import hash_data,verify_hash
from security.jwt_token import JwtTokenCreation
from security.uuid_creation import create_unique_id


class __UserRegisterationInputs:
    def __init__(self,session:Session,name:str,mobile_number:str,email:EmailStr,role:UserRole,password:str):
        self.session=session
        self.name=name
        self.mobile_number=mobile_number
        self.email=email
        self.role=role
        self.password=password

class __UserLoginInputs:
    def __init__(self,session:Session,email_or_no:str|EmailStr,password:str):
        self.session=session
        self.email_or_no=email_or_no
        self.password=password

class __UserForgotInputs:
    def __init__(self,session:Session,email_or_no:str|EmailStr,new_password:str):
        self.session=session
        self.email_or_no=email_or_no
        self.new_password=new_password


class UserVerification:
    def __init__(self,session:Session):
        self.session=session

    async def is_user_not_exists(self,email:EmailStr,mobile_number:str):
        if not self.session.query(exists().where(or_(Users.email==email,Users.mobile_number==mobile_number))).scalar():
            return True
        raise HTTPException(status_code=409,detail="user already exists")
    
    async def is_user_exists(self,email_or_no:EmailStr|str):
       user=self.session.query(Users).filter(or_(Users.email==email_or_no,Users.mobile_number==email_or_no)).first()
       if user:
           return user
       raise HTTPException(status_code=404,detail="user doesn't exists")
    
    async def is_user_exists_by_id(self,id:str):
       user=self.session.query(Users).filter(or_(Users.id==id)).first()
       if user:
           return user
       raise HTTPException(status_code=404,detail="user doesn't exists")
    
class UserRegisteration(__UserRegisterationInputs):
    async def register(self):
        try:
            with self.session.begin():
                #await self.is_user_not_exists()
                user_id=await create_unique_id(self.email)
                user=Users(
                    id=user_id,
                    name=self.name,
                    mobile_number=self.mobile_number,
                    email=self.email,
                    role=self.role,
                    password=await hash_data(self.password)
                )

                self.session.add(user)
                return "user registered successfully"
        
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while register user {e}"
            )

class UserLogin(__UserLoginInputs):
    
    async def login(self,data):
        try:
            user=await UserVerification(session=self.session).is_user_exists(email_or_no=self.email_or_no)
            await verify_hash(hashed_data=user.password,plain_data=self.password)
            data["id"]=user.id
            jwt_token=JwtTokenCreation(
                data=data
            )

            return {
                "access_token":await jwt_token.access_token(),
                "refresh_token":await jwt_token.refresh_token()
            }
        
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
            with self.session.begin():
                self.session.query(Users).filter(or_(Users.email==self.email_or_no,Users.mobile_number==self.email_or_no)).update(
                    {
                        Users.password:await hash_data(self.new_password)
                    }
                )

                return "Successfully password updated"
        
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while updating password {e}"
            )
