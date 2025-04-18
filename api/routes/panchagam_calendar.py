from fastapi import APIRouter,Depends,Response,Query,HTTPException
from api.dependencies.token_verification import verify
from database.main import get_db_session
from database.operations.user_auth import UserVerification,Session
import requests as req
from datetime import date
from icecream import ic

router=APIRouter(
    tags=["Get Panchagm Calendar"]
)

@router.get("/panchagam/calendar")
async def panchagam_calendar_image(date:date=Query(...)):
    #,session:Session=Depends(get_db_session),user:dict=Depends(verify)
    try:
        #await UserVerification(session=session).is_user_exists_by_id(id=user["id"])
        combined_date=f"{date.day}{date.month:02}{date.year}"
        ic(combined_date)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": "https://www.tamildailycalendar.com/"
        }
        url = f"https://www.tamildailycalendar.com/{date.year}/{combined_date}.jpg"
        response=req.get(url,headers=headers)

        if response.status_code==200:
            return Response(
                content=response.content,
                media_type="image/jpg"
            )
        
        raise HTTPException(
            status_code=response.status_code,
            detail="something went wrong while fetching panchagam calendar image"
        )
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
                status_code=500,
                detail=f"something went wrong while fetching panchagam calendar image {e}"
            )
