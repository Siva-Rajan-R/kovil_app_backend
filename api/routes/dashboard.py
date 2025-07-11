from fastapi import APIRouter,requests,Depends,Query
from fastapi.responses import JSONResponse
from database.operations.dashboard import EventDashboard,date,AsyncSession
from database.main import get_db_session
from api.dependencies.token_verification import verify

router=APIRouter(
    tags=["Get Event Dashboard"]
)

@router.get("/event/dashboard")
async def get_dashboard(from_date:date=Query(...),to_date:date=Query(...),session:AsyncSession=Depends(get_db_session),user:dict=Depends(verify)):
    user_id=user["id"]
    return await EventDashboard(
        session=session,
        user_id=user_id,
        from_date=from_date,
        to_date=to_date
    ).get_dashboard()
