from cryptography.fernet import Fernet
import os
# from dotenv import load_dotenv
# load_dotenv()
from fastapi.exceptions import HTTPException
import json
from icecream import ic

SYMETRIC_ENCRYPTION_KEY=os.getenv("SYMETRIC_ENCRYPTION_KEY").encode()

async def encrypt(data:str|dict|list):
    try:
        fernet=Fernet(SYMETRIC_ENCRYPTION_KEY)
        encrypted_data=fernet.encrypt(json.dumps(data).encode()).decode()
        return encrypted_data
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"something went wrong while encrypting data {e}"
        )
    
async def decrypt(encrypted_data:str):
    try:
        fernet=Fernet(SYMETRIC_ENCRYPTION_KEY)
        decrypted_data=json.loads(fernet.decrypt(encrypted_data).decode())
        return decrypted_data
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"something went wrong while decrypting data {e}"
        )
