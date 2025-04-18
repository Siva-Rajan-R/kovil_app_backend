from argon2 import PasswordHasher,exceptions as phexceptions
import os
from dotenv import load_dotenv
load_dotenv() 
from fastapi.exceptions import HTTPException

HASHING_TIME_COST=os.getenv("HASHING_TIME_COST")

ph=PasswordHasher(time_cost=int(HASHING_TIME_COST))

async def hash_data(data:str,hash_salt:bytes=os.urandom(64)):
    try:
        hashed_data=ph.hash(data,salt=hash_salt)
        return hashed_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"something went wrong while hashing data {e}"
        )
    
async def verify_hash(hashed_data,plain_data):
    try:
        ph.verify(hashed_data,plain_data)
        return True
    except phexceptions.VerifyMismatchError:
        raise HTTPException(
            status_code=422,
            detail="invalid data for verifying hash"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"something went wrong while verifying hash {e}"
        )