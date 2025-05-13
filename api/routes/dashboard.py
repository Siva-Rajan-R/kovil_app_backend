from fastapi import APIRouter,requests,Depends,Query
from fastapi.responses import JSONResponse
from database.operations.dashboard import EventDashboard,date,Session
from database.main import get_db_session
from api.dependencies.token_verification import verify

router=APIRouter(
    tags=["Get Event Dashboard"]
)

@router.get("/dashboard")
async def get_dashboard(date:date=Query(...),session:Session=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user["id"]
    return await EventDashboard(
        session=session,
        user_id=user_id,
        date=date
    ).get_dashboard()