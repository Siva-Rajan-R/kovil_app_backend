import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from templates.pyhtml import email_content
from pydantic import EmailStr
import os
from dotenv import load_dotenv
load_dotenv()
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

