from fastapi import APIRouter,Request,Depends,Form,Response,HTTPException,Query,BackgroundTasks
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import EmailStr
from datetime import date,time,datetime
from typing import Optional
from database.main import get_db_session
from database.operations.event_info import EventDropDownValues,AsyncSession
from api.dependencies.token_verification import verify
from security.uuid_creation import create_unique_id
from security.jwt_token import JwtTokenCreation
from security.syme import encrypt,decrypt
from utils.generate_otp import generate_otp
from database.operations.event_crud import AddEvent
from enums.backend_enums import PaymentMode,PaymetStatus
import json
from icecream import ic
from sqlalchemy import RowMapping
from api.dependencies.email_automation import send_booked_event_otp
import textwrap
from api.temp.temp_variabels import generated_client_links


router=APIRouter(
    tags=['Book events']
)

template=Jinja2Templates(directory="templates/client_page")



def serialize_rows(rows: list) -> list[dict]:
    return [dict(row) for row in rows]  # ✅ important

@router.get("/client/event/book/{link_id}",response_class=HTMLResponse)
async def book_events(link_id:str,request:Request,session:AsyncSession=Depends(get_db_session)):
    user_id=generated_client_links.get(link_id,0)
    if user_id:
        event_dd_values=await EventDropDownValues(session=session,user_id="client",isfor_client=True).get_dropdown_values()
        return template.TemplateResponse(name="booking.html",request=request,context={"dd_values":{'event_names':serialize_rows(event_dd_values['event_names']),'neivethiyam_names':serialize_rows(event_dd_values['neivethiyam_names'])},"link_id":link_id})
    raise HTTPException(
        status_code=404,
        detail="link expired please contact event organizer"
    )

@router.post("/client/event/book/confirm/{link_id}")
async def client_event_booking_confirm(
    bgt:BackgroundTasks,
    link_id:str,
    session:AsyncSession=Depends(get_db_session),
    otp:str=Form(...)
):
    booking_info=generated_client_links.get(link_id,0)
    if booking_info:
        if booking_info['otp']==otp:
            ic(booking_info['neivethiyaminfo']['id'])
            await AddEvent(
                user_id=booking_info["user_id"],
                session=session,
                bg_task=bgt,
                event_name=booking_info["eventinfo"]['name'],
                event_description="",
                event_date=booking_info['event_date'],
                event_start_at=booking_info["event_time"],
                event_end_at=booking_info["event_time"],
                client_name=booking_info['client_name'],
                client_mobile_number=booking_info['client_number'],
                client_city=booking_info["client_city"],
                client_email=booking_info['client_email'],
                total_amount=0.0,
                paid_amount=0.0,
                payment_status=PaymetStatus.NOT_PAID,
                payment_mode=PaymentMode.OFFLINE,
                neivethiyam_id=booking_info['neivethiyaminfo']['id'],
                is_special=booking_info['eventinfo']['is_special'],
                padi_kg=booking_info["neivethiyam_kg"],
                is_from_client=True
            ).add_event()
            del generated_client_links[link_id]
            return booking_info
        else:
            attempts=booking_info.get('attempts',0)
            if attempts>=3:
                del generated_client_links[link_id]
                raise HTTPException(
                    status_code=401,
                    detail="You tryed maximum of the attempts, please request a new link to the event manager"
                )
            generated_client_links[link_id]['attempts']=attempts+1
            raise HTTPException(
                status_code=422,
                detail="invalid otp"
            )
    raise HTTPException(
        status_code=404,
        detail="invalid url"
    )

@router.get("/client/event/otp/verify",response_class=HTMLResponse)
def client_event_verify_otp(request:Request,bgt:BackgroundTasks,link_id:str=Query(...)):
    if generated_client_links.get(link_id,0):
        otp=generate_otp()
        generated_client_links[link_id]['otp']=otp
        client_email=generated_client_links[link_id]['client_email']
        bgt.add_task(
            send_booked_event_otp,
            temple_name="Nanmai Tharuvar Kovil (Guruvudhasan)",
            otp=otp,
            to_email=client_email,
            client_name=generated_client_links[link_id]['client_name']
        )
        return template.TemplateResponse(request=request,name="otp.html",context={'link_id':link_id,'otp':otp,'client_email':client_email})
    

@router.post("/client/event/otp/{link_id}")
async def generate_otp_client_event(
    link_id:str,
    request:Request,
    client_name:str=Form(...),
    client_number:str=Form(...),
    client_email:EmailStr=Form(...),
    client_city:str=Form(...),
    eventinfo:str=Form(...),
    neivethiyaminfo:Optional[str]=Form(...),
    neivethiyam_kg:Optional[float]=Form(...),
    event_date:date=Form(...),
    event_time:str=Form(...),
):
    if generated_client_links.get(link_id,0):
        # del generated_client_links[link_id]
        
        ic(json.loads(eventinfo),type(json.loads(eventinfo)))
        ic(event_date,event_time)
        time_obj = datetime.strptime(event_time, "%H:%M")
        time_with_ampm = time_obj.strftime("%I:%M %p")
        ic(time_with_ampm)
        context = {
            "client_name": client_name,
            "client_number": client_number,
            "client_email": client_email,
            "client_city":client_city,
            "eventinfo": json.loads(eventinfo),
            "neivethiyaminfo": json.loads(neivethiyaminfo),
            "neivethiyam_kg": neivethiyam_kg,
            "event_date": event_date,
            "event_time": time_with_ampm,
            "user_id":generated_client_links[link_id]
        }
        generated_client_links[link_id]=context
        print(context)
        return RedirectResponse(url=f"{request.base_url}client/event/otp/verify?link_id={link_id}",status_code=302)
    raise HTTPException(
        status_code=401,
        detail="unautorized or url is invalid"
    )

@router.get("/user/generate/client-link")
async def generate_sharable_client_link(request:Request,user:dict=Depends(verify)):
    user_id=user['id']
    ic(user_id)
    unique_id=await create_unique_id("client")
    generated_client_link=f"{request.base_url}client/event/book/{unique_id}"
    generated_client_links[unique_id]=user_id
    clipboard_format=(
    "🙏 NanmaiTharuvar Kovil (Guruvudhasan) 🙏\n\n"
    "🕉️ Divine Event Booking Invitation\n"
    "தெய்வீக நிகழ்விற்கு பதிவு செய்ய அழைக்கிறோம்\n\n"
    "📌 Kindly use the link below to book your event:\n"
    "தங்களது நிகழ்வை பதிவு செய்ய கீழுள்ள இணைப்பைப் பயன்படுத்தவும்:\n\n"
    f"🔗 {generated_client_link}\n\n"
    "🕒 Note / குறிப்புகள்:\n"
    "Please complete your booking within 15 mins\n"
    "15 minsக்குள் உங்கள் நிகழ்வை பதிவு செய்து உறுதி செய்யவும்"
)
    return {'link':generated_client_link,"exp_time":"15 min",'clipboard_format':clipboard_format}
