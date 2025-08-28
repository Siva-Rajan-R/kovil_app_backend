from pydantic import EmailStr
from textwrap import dedent


def accept_or_forgot_email(name:str,email:EmailStr,number:str,role:str,href:str):
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Email</title>
    <style>
      /* Mobile responsiveness */
      @media only screen and (max-width: 620px) {{
        .container {{
          width: 100% !important;
          padding: 16px !important;
        }}
        .content {{
          font-size: 14px !important;
        }}
        .btn {{
          width: 100% !important;
          display: block !important;
          text-align: center !important;
        }}
        .stack td {{
          display: block !important;
          width: 100% !important;
          text-align: left !important;
          padding: 6px 0 !important;
        }}
      }}
    </style>
  </head>
  <body style="margin:0;padding:20px 0;background-color:#fff8f0;font-family:Arial, sans-serif;">
    <center>
      <table cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="#fff8f0">
        <tr>
          <td align="center">
            <table cellpadding="0" cellspacing="0" border="0" class="container" style="max-width:600px;width:100%;background:linear-gradient(to bottom,#fff7dc,#ffe4c4);border-radius:12px;border:1px solid #f6d27e;box-shadow:0 4px 10px rgba(0,0,0,0.1);">
              <tr>
                <td style="padding:30px 40px;" class="content">

                  <!-- Main Title -->
                  <h1 style="font-size:26px;font-weight:800;color:#7c2d12;text-align:center;margin:0 0 8px 0;">
                    Guruvudhasaan
                  </h1>
                  <h2 style="font-size:18px;font-weight:600;color:#b45309;text-align:center;margin:0 0 24px 0;">
                    Nanmai Tharuvar Kovil
                  </h2>

                  <hr style="border:none;border-top:2px solid #f6d27e;margin:20px 0;" />

                  <!-- Employee Info -->
                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:12px;" class="stack">
                    <tr>
                      <td style="color:#78350f;font-weight:600;font-size:14px;">Employee Name:</td>
                      <td style="color:#7c2d12;font-weight:700;font-size:16px;" align="right">{name}</td>
                    </tr>
                  </table>

                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:12px;border-top:1px solid #f6d27e;padding-top:12px;" class="stack">
                    <tr>
                      <td style="color:#78350f;font-weight:600;font-size:14px;">Email:</td>
                      <td style="color:#7c2d12;font-weight:700;font-size:16px;" align="right">{email}</td>
                    </tr>
                  </table>

                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:12px;border-top:1px solid #f6d27e;padding-top:12px;" class="stack">
                    <tr>
                      <td style="color:#78350f;font-weight:600;font-size:14px;">Mobile Number:</td>
                      <td style="color:#7c2d12;font-weight:700;font-size:16px;" align="right">{number}</td>
                    </tr>
                  </table>

                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:12px;border-top:1px solid #f6d27e;padding-top:12px;" class="stack">
                    <tr>
                      <td style="color:#78350f;font-weight:600;font-size:14px;">Applied Role:</td>
                      <td style="color:#7c2d12;font-weight:700;font-size:16px;" align="right">{role}</td>
                    </tr>
                  </table>

                  <!-- Accept Button -->
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="text-align:center; padding-top:28px;">
                        <a href="{href}" style="display:inline-block;background-color:#ea580c;color:#ffffff;text-decoration:none;padding:12px 28px;border-radius:8px;font-weight:bold;font-size:18px;text-align:center;">
                          Accept
                        </a>
                      </td>
                    </tr>
                  </table>

                  <!-- Footer -->
                  <p style="color:#7c2d12;text-align:center;margin-top:24px;font-size:14px;line-height:1.5;">
                    If you're not accepting this then leave it alone!<br />
                    It will expire in 120 sec
                  </p>

                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </center>
  </body>
</html>

"""

def register_or_forgot_successfull_email(email_subject:str,email_body:str):
    return f"""
<!DOCTYPE html>
<html lang="en">
<body style="margin:0; padding:20px 0; font-family: Arial, sans-serif; background-color: #fff8f0; display:flex; justify-content:center; align-items:center; min-height:100vh;">
    <!--[if mso]>
    <center>
    <table cellpadding="0" cellspacing="0"><tr><td width="600">
    <![endif]-->
    <div style="max-width:600px; margin:0 auto;">
        <table cellpadding="0" cellspacing="0" style="width:100%; background:linear-gradient(to bottom, #fff7dc, #ffe4c4); border-radius:12px; border-collapse:separate; border:1px solid #f6d27e;">
            <!-- Header -->
            <tr>
                <td style="padding:24px 20px; text-align:center;">
                    <h1 style="font-size:26px; color:#7c2d12; margin:0; font-weight:800;">
                        Guruvudhasaan
                    </h1>
                    <h2 style="font-size:18px; color:#b45309; margin:8px 0 0 0; font-weight:600;">
                        Nanmai Tharuvar Kovil
                    </h2>
                </td>
            </tr>
            
            <!-- Divider -->
            <tr>
                <td style="padding:0 20px;">
                    <hr style="border:none; border-top:2px solid #f6d27e; margin:16px 0;" />
                </td>
            </tr>

            <!-- Body -->
            <tr>
                <td style="padding:20px; text-align:left; color:#7c2d12; font-size:16px; line-height:1.6;">
                    <p style="margin:0 0 16px 0; font-weight:700; font-size:16;">{email_body}</p>
                </td>
            </tr>

            <!-- Footer -->
            <tr>
                <td style="padding:24px 20px; text-align:center;">
                    <p style="margin:0; font-size:14px; color:#b45309;">
                        This is an official message from Guruvudhasaan - Nanmai Tharuvar Kovil
                    </p>
                </td>
            </tr>
        </table>
    </div>
    <!--[if mso]>
    </td></tr></table>
    </center>
    <![endif]-->
</body>
</html>


"""

def booked_event_successfull_email(name, poojai_type, date, time, temple_name, address):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🕉️ Poojai Booking Confirmed</title>
<style>
  body {{
    margin: 0;
    font-family: Arial, sans-serif;
    background-color: #fef7f0;
  }}
  .container {{
    max-width: 600px;
    margin: 20px auto;
    background-color: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(123, 44, 191, 0.1);
  }}
  .header {{
    background: linear-gradient(135deg, #7b2cbf, #5a189a);
    color: white;
    text-align: center;
    padding: 30px 20px;
  }}
  .header h1 {{
    margin: 0;
    font-size: 24px;
  }}
  .content {{
    padding: 30px;
    color: #2b2d42;
  }}
  .detail-label {{
    font-weight: bold;
    color: #5a189a;
    display: inline-block;
    width: 130px;
  }}
  .btn {{
    display: inline-block;
    background: #7b2cbf;
    color: white;
    text-decoration: none;
    padding: 12px 25px;
    border-radius: 8px;
    font-weight: 500;
    margin-top: 20px;
    text-align: center;
  }}
  .footer {{
    background: #f9f5ff;
    color: #6c757d;
    text-align: center;
    padding: 15px;
    font-size: 13px;
  }}
</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🕉️ Poojai Booking Confirmed</h1>
      <p>{temple_name}</p>
    </div>
    <div class="content">
      <p>Dear <strong>{name}</strong>,</p>
      <p>Your poojai booking has been confirmed. May divine blessings be with you and your family.</p>
      <h3>Booking Details</h3>
      <p><span class="detail-label">Poojai Type:</span> {poojai_type}</p>
      <p><span class="detail-label">Date & Time:</span> {date} at {time}</p>
      <p><span class="detail-label">Venue:</span> {temple_name}, {address}</p>
      <p>📝 <strong>Important Notes:</strong></p>
      <ul>
        <li>Arrive 15 minutes before the scheduled time</li>
        <li>Traditional attire is recommended</li>
        <li>Bring your receipt for verification</li>
      </ul>
    </div>
    <div class="footer">
      © 2025 {temple_name}. All rights reserved.
    </div>
  </div>
</body>
</html>
"""


def booked_event_canceled_email(customer_name, poojai_name, date, time, reason, temple_name, reschedule_link):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>🕉️ Poojai Booking Cancellation</title>
<style>
  body {{
    margin: 0;
    font-family: Arial, sans-serif;
    background-color: #fff5f5;
    color: #2b2d42;
  }}
  .container {{
    max-width: 600px;
    margin: 20px auto;
    background-color: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(123, 44, 191, 0.1);
  }}
  .header {{
    background: linear-gradient(135deg, #ff6b6b, #d32f2f);
    color: white;
    text-align: center;
    padding: 30px 20px;
  }}
  .header h1 {{
    margin: 0;
    font-size: 24px;
  }}
  .content {{
    padding: 30px;
  }}
  .detail-label {{
    font-weight: bold;
    color: #d32f2f;
    display: inline-block;
    width: 130px;
  }}
  .btn {{
    display: inline-block;
    background: #7b2cbf;
    color: white;
    text-decoration: none;
    padding: 12px 25px;
    border-radius: 8px;
    font-weight: 500;
    margin-top: 20px;
  }}
  .footer {{
    background: #f9f5ff;
    color: #6c757d;
    text-align: center;
    padding: 15px;
    font-size: 13px;
  }}
</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🕉️ Poojai Booking Cancelled</h1>
      <p>{temple_name}</p>
    </div>
    <div class="content">
      <p>Dear <strong>{customer_name}</strong>,</p>
      <p>Your scheduled poojai <strong>{poojai_name}</strong> on {date} at {time} has been cancelled due to <strong>{reason}</strong>.</p>
      <h3>Booking Details</h3>
      <p><span class="detail-label">Poojai Type:</span> {poojai_name}</p>
      <p><span class="detail-label">Date & Time:</span> {date} at {time}</p>
      <p><span class="detail-label">Reason:</span> {reason}</p>
      <p>We apologize for the inconvenience. <strong>we will refund your amount within 7 working days</strong></p>
    </div>
    <div class="footer">
      © 2025 {temple_name}. All rights reserved.
    </div>
  </div>
</body>
</html>
"""



def booked_event_completed_email(client_name, date, time, poojai_name, description, temple_name):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🕉️ Poojai Successfully Completed</title>
<style>
  body {{
    margin: 0;
    font-family: Arial, sans-serif;
    background-color: #f0fdf4;
    color: #2b2d42;
  }}
  .container {{
    max-width: 600px;
    margin: 20px auto;
    background-color: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(123, 44, 191, 0.1);
  }}
  .header {{
    background: linear-gradient(135deg, #4caf50, #2e7d32);
    color: white;
    text-align: center;
    padding: 30px 20px;
  }}
  .header h1 {{
    margin: 0;
    font-size: 24px;
  }}
  .content {{
    padding: 30px;
  }}
  .detail-label {{
    font-weight: bold;
    color: #2e7d32;
    display: inline-block;
    width: 130px;
  }}
  .btn {{
    display: inline-block;
    background: #4caf50;
    color: white;
    text-decoration: none;
    padding: 12px 25px;
    border-radius: 8px;
    font-weight: 500;
    margin-top: 20px;
  }}
  .footer {{
    background: #f9f5ff;
    color: #6c757d;
    text-align: center;
    padding: 15px;
    font-size: 13px;
  }}
</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🕉️ Poojai Successfully Completed</h1>
      <p>{temple_name}</p>
    </div>
    <div class="content">
      <p>Dear <strong>{client_name}</strong>,</p>
      <p>Your poojai <strong>{poojai_name}</strong> performed on {date} at {time} has been completed successfully with devotion.</p>
      <h3>Poojai Details</h3>
      <p><span class="detail-label">Poojai Type:</span> {poojai_name}</p>
      <p><span class="detail-label">Performed On:</span> {date} at {time}</p>
      <p><span class="detail-label">Offering:</span> {description}</p>
      <p>🙏 Thank you for choosing <strong>{temple_name}</strong> for your spiritual journey.</p>
      <p>🌺 We hope divine blessings fill your life with peace, happiness, and prosperity.</p>
    </div>
    <div class="footer">
      © 2025 {temple_name}. All rights reserved.
    </div>
  </div>
</body>
</html>
"""



def booking_otp_email(temple_name,client_name,otp):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OTP Verification</title>
  <style>
    body {{
      font-family: 'Poppins', Arial, sans-serif;
      line-height: 1.6;
      color: #2b2d42;
      background-color: #f8f4ff;
      margin: 0;
      padding: 0;
    }}
    
    .email-container {{
      max-width: 600px;
      margin: 0 auto;
      background: white;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 4px 15px rgba(123, 44, 191, 0.1);
    }}
    
    .header {{
      background: linear-gradient(135deg, #7b2cbf, #5a189a);
      padding: 25px 20px;
      text-align: center;
      color: white;
    }}
    
    .header h1 {{
      margin: 0;
      font-size: 22px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
    }}
    
    .content {{
      padding: 25px;
    }}
    
    .greeting {{
      font-size: 16px;
      margin-bottom: 20px;
    }}
    
    .otp-box {{
      background: #f3e5ff;
      border-radius: 8px;
      padding: 25px;
      text-align: center;
      margin: 20px 0;
      border: 1px dashed #9d4edd;
    }}
    
    .otp-code {{
      font-size: 32px;
      letter-spacing: 8px;
      color: #5a189a;
      font-weight: 700;
      margin: 15px 0;
      font-family: monospace;
    }}
    
    .divider {{
      border-top: 1px dashed #e0aaff;
      margin: 20px 0;
    }}
    
    .footer {{
      text-align: center;
      padding: 15px;
      font-size: 13px;
      color: #6c757d;
      background: #f9f5ff;
    }}
    
    .icon {{
      color: #7b2cbf;
      margin-right: 8px;
      vertical-align: middle;
    }}
    
    .note {{
      font-size: 14px;
      color: #d32f2f;
      background: #ffebee;
      padding: 10px;
      border-radius: 6px;
      margin: 15px 0;
    }}
    
    @media only screen and (max-width: 600px) {{
      .content {{
        padding: 20px;
      }}
      .otp-code {{
        font-size: 28px;
        letter-spacing: 5px;
      }}
    }}
  </style>
</head>
<body>
  <div class="email-container">
    <div class="header">
      <h1><span>🔐</span> Your OTP for Poojai Booking</h1>
    </div>
    
    <div class="content">
      <div class="greeting">
        <p>Dear {client_name},</p>
        <p>Please use the following One-Time Password (OTP) to verify your identity for your poojai booking at <strong>{temple_name}</strong>:</p>
      </div>
      
      <div class="otp-box">
        <p style="margin:0 0 10px 0;font-weight:500">Your verification code:</p>
        <div class="otp-code">{otp}</div>
        <p style="margin:10px 0 0 0;font-size:14px">Valid for <strong>15 minutes</strong> only</p>
      </div>
      
      <div class="note">
        <span class="icon">⚠️</span> <strong>Security Note:</strong> Never share this OTP with anyone, including temple staff.
      </div>
      
      
      <div class="divider"></div>
      
      <p style="font-size:14px">If you didn't request this OTP, please ignore this email.</p>
      
      <p>With divine blessings,<br>The {temple_name} Team</p>
    </div>
    
    <div class="footer">
      <p>© 2023 {temple_name}. All rights reserved.</p>
      <p>May the divine light guide you always</p>
    </div>
  </div>
</body>
</html>
"""
