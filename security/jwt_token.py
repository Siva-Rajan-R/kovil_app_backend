import jwt
from datetime import datetime,timezone,timedelta
from fastapi.exceptions import HTTPException
from security.syme import encrypt,decrypt
import os
from dotenv import load_dotenv
load_dotenv()
from icecream import ic

JWT_TOKEN_EXPIRY_IN_MINUTES=int(os.getenv("JWT_TOKEN_EXPIRY_IN_MINUTES"))
JWT_TOKEN_EXPIRY_IN_DAYS=int(os.getenv("JWT_TOKEN_EXPIRY_IN_DAYS"))
ACCESS_TOKEN_JWT_KEY=os.getenv("ACCESS_TOKEN_JWT_KEY")
REFRESH_TOKEN_JWT_KEY=os.getenv("REFRESH_TOKEN_JWT_KEY")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")

class JwtTokenCreation:
    def __init__(self,data:dict):
        self.data=data

    async def access_token(self):
        try:
            encrypted_data=await encrypt(data=self.data)
            data={
                "exp":datetime.now(timezone.utc)+timedelta(minutes=JWT_TOKEN_EXPIRY_IN_MINUTES),
                "data":encrypted_data
            }

            return jwt.encode(data,key=ACCESS_TOKEN_JWT_KEY,algorithm=JWT_ALGORITHM)
        
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while creating access token {e}"
            )
    
    async def refresh_token(self):
        try:
            encrypted_data=await encrypt(data=self.data)
            data={
                "exp":datetime.now(timezone.utc)+timedelta(days=JWT_TOKEN_EXPIRY_IN_DAYS),
                "data":encrypted_data
            }

            return jwt.encode(data,key=REFRESH_TOKEN_JWT_KEY,algorithm=JWT_ALGORITHM)
        
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while creating access token {e}"
            )

class JwtTokenVerification:
    async def verify_access_token(self,access_token:str,data:dict):
        try:
            decoded_data=jwt.decode(access_token,key=ACCESS_TOKEN_JWT_KEY,algorithms=JWT_ALGORITHM)
            decrypted_data=await decrypt(decoded_data["data"])
            data.update({"id":decrypted_data["id"]})
            
            if decrypted_data==data:
                return decrypted_data
            
            raise HTTPException(
                status_code=401,
                detail="invalid access token"
            )
        
        except HTTPException:
            raise

        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="token has expired"
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while verifying access token {e}"
            )
        
    async def get_new_access_token(self,refresh_token:str,data:dict):
        try:
            print(refresh_token)
            decoded_data=jwt.decode(refresh_token,key=REFRESH_TOKEN_JWT_KEY,algorithms=JWT_ALGORITHM)
            
            decrypted_data=await decrypt(decoded_data["data"])
            data.update({"id":decrypted_data["id"]})
            if decrypted_data==data:
                
                return await JwtTokenCreation(decrypted_data).access_token()
            raise HTTPException(
                status_code=401,
                detail="invalid refresh token"
            )
        
        except HTTPException:
            raise

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while getting new access token {e}"
            )
        