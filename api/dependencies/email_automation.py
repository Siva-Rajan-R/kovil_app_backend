import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from templates.pyhtml import email_content
from email.message import EmailMessage
import mimetypes
from pydantic import EmailStr
import os
from io import BytesIO
import pandas as pd

# from dotenv import load_dotenv
# load_dotenv()
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ADMIN_EMAIL=os.getenv("ADMIN_EMAIL")

async def accept_or_forgot_email(email_subject:str,name:str,email:EmailStr,number:str,role:str,href:str,isforgot:bool=False):
    html_content = email_content.accept_or_forgot_email(name=name,email=email,number=number,role=role,href=href)

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ADMIN_EMAIL
    msg["Subject"] = email_subject
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        if isforgot:
            server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
            msg["To"] = email
        else:
            server.sendmail(EMAIL_ADDRESS, ADMIN_EMAIL, msg.as_string())

    print("Email sent successfully!")


def register_or_forgot_successfull_email(email_subject:str,email_body:str,email:EmailStr):
    html_content=email_content.register_or_forgot_successfull_email(email_subject=email_subject,email_body=email_body)
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email
    msg["Subject"] = email_subject
    msg.attach(MIMEText(html_content, "html"))

    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, msg.as_string())

    print("Email sent successfully!")




def send_events_report_as_excel(to_email: EmailStr, events: list[dict],excel_filename:str,is_contains_image:bool):
    msg = EmailMessage()
    msg['Subject'] = 'Nanmai tharuvar kovil Events report as EXCEL'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content('Please find the attached images and Excel document.')

    # Attach images
    if is_contains_image:
        for idx, event in enumerate(events):
            if event.get('image'):
                image_path = f"eventReport-Image-{idx}.jpg"
                msg.add_attachment(event['image'], maintype="image", subtype="jpg", filename=image_path)
    # Generate Excel in memory
    buffer = BytesIO()
    
    df = pd.DataFrame(events)
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0)

    msg.add_attachment(
        buffer.read(),
        maintype='application',
        subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        filename=excel_filename
    )

    # Send mail
    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def send_event_report_as_pdf(to_email: EmailStr, pdf_bytes: bytes,pdf_filename:str):
    msg = EmailMessage()
    msg['Subject'] = 'Nanmai tharuvar kovil Events report as PDF'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content('Please find the attached PDF document.')

    msg.add_attachment(
        pdf_bytes,
        maintype='application',
        subtype='pdf',
        filename=pdf_filename
    )

    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def event_booked_successfull_report(name, poojai_type, date, time, temple_name, address,to_email):
    html_content=email_content.booked_event_successfull_email(name, poojai_type, date, time, temple_name, address,)
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = "Your Event booked successfully"
    msg.attach(MIMEText(html_content, "html"))

    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())

    print("Email sent successfully!")

def event_booked_canceled_report(name, poojai_type, date, time, reason,temple_name,reschedule_link,to_email):
    try:
        print("ulla bro")
        html_content=email_content.booked_event_canceled_email(customer_name=name,poojai_name=poojai_type,date=date,time=time,reason=reason,temple_name=temple_name,reschedule_link=reschedule_link)
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = "Your Event booking canceled"
        msg.attach(MIMEText(html_content, "html"))

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print(e)

def event_booked_completed_report(name,event_name, date, time, description,temple_name,to_email):
    try:
        print("ulla bro")
        html_content=email_content.booked_event_completed_email(poojai_name=event_name,client_name=name,date=date,time=time,description=description,temple_name=temple_name)
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = "Your Event completed successfully"
        msg.attach(MIMEText(html_content, "html"))

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print(e)

def send_booked_event_otp(temple_name,client_name,otp,to_email):
    try:
        print("ulla bro")
        html_content=email_content.booking_otp_email(temple_name=temple_name,otp=otp,client_name=client_name)
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = "Your Event booking OTP"
        msg.attach(MIMEText(html_content, "html"))

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print(e)
# event_booked_canceled_report("","","","","","","","siva967763@gmail.com")