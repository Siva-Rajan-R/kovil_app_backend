import uuid
from fastapi.exceptions import HTTPException
async def create_unique_id(data:str):
    try:
        return str(uuid.uuid5(uuid.uuid4(),data))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"something went wrong while creating uuid {e}"
        )