import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from templates.pyhtml import email_content
from email.message import EmailMessage
import mimetypes
from pydantic import EmailStr
import os

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


async def send_events_report_as_excel(to_email:EmailStr,events:list[dict],excel_file:str):

    msg = EmailMessage()
    msg['Subject'] = 'Nanmai tharuvar kovil Events report as EXCEL'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content('Please find the attached images and Excel document.')

    # Attach multiple images
    # image_files = ['img1.jpg', 'img2.png']
    print("hello1")
    for index,image_data in enumerate(events):
        image_path=f"eventReport-Image-{index}.jpg"
        print(image_path)
        msg.add_attachment(image_data['image'], maintype="image", subtype="jpg", filename=image_path)
    print("hello")
    # Attach Excel file
    excel_path = excel_file
    with open(excel_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=excel_file)

    # Send the email
    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    
    print("Email sent successfully!")

async def send_event_report_as_pdf(to_email:EmailStr,pdf_file:str):
    msg = EmailMessage()
    msg['Subject'] = 'Nanmai tharuvar kovil Events report as PDF'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content('Please find the attached images and Excel document.')

    pdf_path=pdf_file
    with open(pdf_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=pdf_file)

    # Send the email
    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    
    print("Email sent successfully!")