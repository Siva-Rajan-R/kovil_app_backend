from fastapi import FastAPI
from api.routes import dashboard, event_crud, user_auth ,event_info,user_crud,panchagam_calendar,workers_crud

app=FastAPI()

app.include_router(user_auth.router)
app.include_router(user_crud.router)
app.include_router(event_crud.router)
app.include_router(event_info.router)
app.include_router(dashboard.router)
app.include_router(panchagam_calendar.router)
app.include_router(workers_crud.router)
