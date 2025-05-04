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

async def accept_or_forgot_email(email_subject:str,name:str,email:EmailStr,number:str,href:str,isforgot:bool=False):
    html_content = email_content.accept_or_forgot_email(name=name,email=email,number=number,href=href)

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




async def send_events_report_as_excel(to_email: EmailStr, events: list[dict],excel_filename:str):
    msg = EmailMessage()
    msg['Subject'] = 'Nanmai tharuvar kovil Events report as EXCEL'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content('Please find the attached images and Excel document.')

    # Attach images
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


async def send_event_report_as_pdf(to_email: EmailStr, pdf_bytes: bytes,pdf_filename:str):
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
