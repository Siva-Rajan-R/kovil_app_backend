from pydantic import EmailStr
from textwrap import dedent


def accept_or_forgot_email(name:str,email:EmailStr,number:str,role:str,href:str):
    return f"""
    <html>
    <div style="min-height:100vh;display:flex;justify-content:center;align-items:center;width:100%;margin:0;padding:20px 0;background:#f5f5f5;">
  <!--[if mso]>
  <center>
  <table cellpadding="0" cellspacing="0"><tr><td width="600">
  <![endif]-->
  <div style="max-width:600px;margin:0 auto;">
    <table cellpadding="0" cellspacing="0" style="width:100%;background:#000435;border-radius:6px;border-collapse:separate;">
      <tr>
        <td style="padding:32px 40px;">
          <h1 style="font-size:24px;color:#34e0f7;text-align:center;margin:0 0 20px 0;font-family:Arial,sans-serif;">
            Nanmai Tharuvar Kovil
          </h1>
          
          <table cellpadding="0" cellspacing="0" style="width:100%;border-top:1px solid white;margin:20px 0;"></table>
          <tr>
              <td style="padding:16px 0;">
                <table cellpadding="0" cellspacing="0">
                  <tr>
                    <td style="padding-right:15px;color:#34e0f7;font-weight:bold;font-family:Arial,sans-serif;">
                      <h2><b>Employee Name:</b></h2>
                    </td>
                    <td style="color:white;font-family:Arial,sans-serif;">
                      <h2><b>{name}</b></h2>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          <table cellpadding="0" cellspacing="0" style="width:100%;">
            <tr>
              <td style="padding:16px 0;border-bottom:1px solid rgba(255,255,255,0.1);">
                <table cellpadding="0" cellspacing="0">
                  <tr>
                    <td style="padding-right:15px;color:#34e0f7;font-weight:bold;font-family:Arial,sans-serif;">
                      <h2><b>Email:</b></h2>
                    </td>
                    <td style="color:white;font-family:Arial,sans-serif;">
                      <h2><b>{email}</b></h2>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <table cellpadding="0" cellspacing="0" style="width:100%;">
            <tr>
              <td style="padding:16px 0;border-bottom:1px solid rgba(255,255,255,0.1);">
                <table cellpadding="0" cellspacing="0">
                  <tr>
                    <td style="padding-right:15px;color:#34e0f7;font-weight:bold;font-family:Arial,sans-serif;">
                      <h2><b>Mobile Number:</b></h2>
                    </td>
                    <td style="color:white;font-family:Arial,sans-serif;">
                      <h2><b>{number}</b></h2>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding:16px 0;">
                <table cellpadding="0" cellspacing="0">
                  <tr>
                    <td style="padding-right:15px;color:#34e0f7;font-weight:bold;font-family:Arial,sans-serif;">
                      <h2><b>Applied Role:</b></h2>
                    </td>
                    <td style="color:white;font-family:Arial,sans-serif;">
                      <h2><b>{role}</b></h2>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>

          <div style="text-align:center;margin:32px 0;">
            <a href="{href}" style="display:inline-block;background:#34e0f7;color:#000435;text-decoration:none;padding:12px 24px;border-radius:6px;font-weight:bold;font-family:Arial,sans-serif;font-size:20px">
              Accept
            </a>
          </div>

          <p style="color:white;text-align:center;margin:20px 0 0 0;font-family:Arial,sans-serif;">
            If you're not accepting this then leave it alone!,it will expired in 120 sec
          </p>
        </td>
      </tr>
    </table>
  </div>
  <!--[if mso]>
  </td></tr></table>
  </center>
  <![endif]-->
</div>
</html>
    """

def register_or_forgot_successfull_email(email_subject:str,email_body:str):
    return f"""
<!DOCTYPE html>
<html lang="en">
<body style="margin: 0; padding: 20px 0; font-family: Arial, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; min-height: 100vh;">
    <!--[if mso]>
    <center>
    <table cellpadding="0" cellspacing="0"><tr><td width="600">
    <![endif]-->
    <div style="max-width:600px; margin:0 auto;">
        <table cellpadding="0" cellspacing="0" style="width:100%; background:#000435; border-radius:6px; border-collapse:separate;">
            <tr>
                <td style="padding:32px 40px; text-align:center;">
                    <h1 style="font-size:24px; color:#34e0f7; margin:0 0 20px 0; font-family:Arial,sans-serif;">
                        {email_subject}
                    </h1>
                    <table cellpadding="0" cellspacing="0" style="width:100%; border-top:1px solid white; margin:20px 0;"></table>
                    <p style="font-size:16px; line-height:1.5; color:white; font-family:Arial,sans-serif;">
                        {email_body}
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

def booked_event_successfull_email(name, poojai_type, date, time, temple_name, address,):
  return dedent(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Poojai Booking Confirmation</title>
      <style>
        body {{
          font-family: 'Poppins', Arial, sans-serif;
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
          padding: 30px 20px;
          text-align: center;
          color: white;
        }}
        .content {{
          padding: 30px;
          color: #2b2d42;
        }}
        .detail-label {{
          font-weight: bold;
          color: #5a189a;
          width: 120px;
          display: inline-block;
        }}
        .btn {{
          display: inline-block;
          background: #7b2cbf;
          color: white;
          text-decoration: none;
          padding: 12px 25px;
          border-radius: 8px;
          font-weight: 500;
          margin-top: 15px;
        }}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="header">
          <h1>🕉️ Poojai Booking Confirmed</h1>
        </div>
        <div class="content">
          <p>Dear {name},</p>
          <p>We are delighted to confirm your poojai booking. May divine blessings be with you and your family.</p>

          <h3>Booking Details</h3>
          <p><span class="detail-label">Poojai Type:</span> {poojai_type}</p>
          <p><span class="detail-label">Date & Time:</span> {date} at {time}</p>

          <br>
          <p>📌 <strong>Venue:</strong> {temple_name}, {address}</p>

          <p>📝 <strong>Important Notes:</strong></p>
          <ul>
            <li>Please arrive 15 minutes before the scheduled time</li>
            <li>Traditional attire is recommended</li>
            <li>Bring your receipt for verification</li>
          </ul>

          <p>If you have any queries, contact us at <a href="mailto:poojai@temple.com">poojai@temple.com</a> or call +91 XXXXX XXXXX.</p>

          <p>With divine blessings,<br>The {temple_name} Team</p>
        </div>
        <div class="footer" style="padding:20px; font-size:13px; text-align:center; color:#888;">
          <p>© 2025 {temple_name}. All rights reserved.</p>
          <p>Follow us on your spiritual journey: [Social Links]</p>
        </div>
      </div>
    </body>
    </html>
    """)

def booked_event_canceled_email(
    customer_name: str,
    poojai_name: str,
    date: str,
    time: str,
    reason: str,
    temple_name: str,
    reschedule_link: str
) :
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Poojai Cancellation Notification</title>
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
      margin: auto;
      background: white;
      border-radius: 8px;
      box-shadow: 0 4px 15px rgba(123, 44, 191, 0.1);
      overflow: hidden;
    }}
    .header {{
      background: linear-gradient(135deg, #7b2cbf, #5a189a);
      padding: 30px 20px;
      text-align: center;
      color: white;
    }}
    .header h1 {{
      margin: 0;
      font-size: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
    }}
    .content {{
      padding: 30px;
    }}
    .greeting {{
      font-size: 18px;
      margin-bottom: 25px;
    }}
    .cancellation-details {{
      background: #fff5f5;
      border-left: 4px solid #ff6b6b;
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 25px;
    }}
    .detail-row {{
      display: flex;
      margin-bottom: 12px;
    }}
    .detail-label {{
      font-weight: 600;
      width: 130px;
      color: #5a189a;
    }}
    .divider {{
      border-top: 1px dashed #e0aaff;
      margin: 25px 0;
    }}
    .footer {{
      text-align: center;
      padding: 20px;
      font-size: 14px;
      color: #6c757d;
      background: #f9f5ff;
    }}
    .icon {{
      color: #7b2cbf;
      margin-right: 10px;
    }}
    .btn {{
      display: inline-block;
      background: #7b2cbf;
      color: white;
      text-decoration: none;
      padding: 12px 25px;
      border-radius: 8px;
      font-weight: 500;
      margin-top: 15px;
    }}
    .btn:hover {{
      background: #5a189a;
    }}
    @media only screen and (max-width: 600px) {{
      .content {{
        padding: 20px;
      }}
      .detail-row {{
        flex-direction: column;
      }}
      .detail-label {{
        margin-bottom: 5px;
        width: auto;
      }}
    }}
  </style>
</head>
<body>
  <div class="email-container">
    <div class="header">
      <h1><span>🕉️</span> Poojai Booking Cancellation</h1>
    </div>
    <div class="content">
      <div class="greeting">
        <p>Dear {customer_name},</p>
        <p>We regret to inform you that your scheduled poojai has been cancelled due to <strong>{reason}</strong>. Please accept our sincere apologies for any inconvenience caused.</p>
      </div>

      <div class="cancellation-details">
        <h3 style="margin-top: 0; color: #d32f2f;">Cancellation Details</h3>
        <div class="detail-row">
          <div class="detail-label">Poojai Type: </div>
          <div> {poojai_name}</div>
        </div>
        <div class="detail-row">
          <div class="detail-label">Scheduled Date: </div>
          <div> {date} at {time}</div>
        </div>
        <div class="detail-row">
          <div class="detail-label">Reason: </div>
          <div><strong> {reason}</strong></div>
        </div>
        <div class="detail-row">
          <div class="detail-label">Refund Status: </div>
          <div> If any of the payment made ,Full refund will be processed within 5–7 business days.</div>
        </div>
      </div>

      <p><span class="icon">🔄</span> <strong>We would love to reschedule:</strong> Please reply to this number 1234567890 to arrange a new date.</p>

      <p><span class="icon">🙏</span> <strong>Our Apologies: </strong> We understand the spiritual significance of your booking and deeply regret this cancellation.</p>

      <div class="divider"></div>

      <p>For any questions, please contact our support team at <a href="mailto:support@temple.com">support@temple.com</a>.</p>

      <p>With sincere apologies,<br>The {temple_name} Team</p>

      <a href="{reschedule_link}" class="btn" style="background:#7b2cbf;color:white;text-decoration:none;padding:12px 25px;border-radius:8px;display:inline-block;font-weight:500;">Reschedule Your Poojai</a>
    </div>

    <div class="footer">
      <p>© 2025 {temple_name}. All rights reserved.</p>
      <p>May divine blessings be with you.</p>
    </div>
  </div>
</body>
</html>"""


def booked_event_completed_email(client_name,date,time,poojai_name,description,temple_name):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Poojai Successfully Completed</title>
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
      background: linear-gradient(135deg, #4CAF50, #2E7D32);
      padding: 30px 20px;
      text-align: center;
      color: white;
    }}

    .header h1 {{
      margin: 0;
      font-size: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
    }}
    
    .content {{
      padding: 30px;
    }}
    
    .greeting {{
      font-size: 18px;
      margin-bottom: 25px;
    }}
    
    .completion-details {{
      background: #f1f8e9;
      border-left: 4px solid #4CAF50;
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 25px;
    }}
    
    .detail-row {{
      display: flex;
      margin-bottom: 12px;
    }}
    
    .detail-label {{
      font-weight: 600;
      width: 120px;
      color: #2E7D32;
    }}
    
    .divider {{
      border-top: 1px dashed #a5d6a7;
      margin: 25px 0;
    }}
    
    .footer {{
      text-align: center;
      padding: 20px;
      font-size: 14px;
      color: #6c757d;
      background: #f9f5ff;
    }}
    
    .icon {{
      color: #2E7D32;
      margin-right: 10px;
    }}
    
    .btn {{
      display: inline-block;
      background: #4CAF50;
      color: white;
      text-decoration: none;
      padding: 12px 25px;
      border-radius: 8px;
      font-weight: 500;
      margin-top: 15px;
    }}
    
    .btn:hover {{
      background: #2E7D32;
    }}
    
    .blessing {{
      font-style: italic;
      color: #5a189a;
      text-align: center;
      margin: 20px 0;
      font-size: 1.1rem;
    }}
    
    @media only screen and (max-width: 600px) {{
      .content {{
        padding: 20px;
      }}
      
      .detail-row {{
        flex-direction: column;
      }}
      
      .detail-label {{
        margin-bottom: 5px;
        width: auto;
      }}
    }}
  </style>
</head>
<body>
  <div class="email-container">
    <div class="header">
      <h1><span>🕉️</span> Poojai Successfully Completed</h1>
    </div>
    
    <div class="content">
      <div class="greeting">
        <p>Dear {client_name},</p>
        <p>We are delighted to inform you that your [Poojai Name] was performed with full rituals and devotion. May the divine blessings bring peace and prosperity to you and your family.</p>
      </div>
      
      <div class="blessing">
        "May the divine grace of the Almighty be with you always."
      </div>
      
      <div class="completion-details">
        <h3 style="margin-top: 0; color: #2E7D32;">Poojai Details</h3>
        
        <div class="detail-row">
          <div class="detail-label">Poojai Type:</div>
          <div>{poojai_name}</div>
        </div>
        
        <div class="detail-row">
          <div class="detail-label">Performed On:</div>
          <div>{date} at {time}</div>
        </div>
        
        
        <div class="detail-row">
          <div class="detail-label">Offering:</div>
          <div>{description}</div>
        </div>
      </div>
      
      <div class="divider"></div>
      
      <p>We sincerely thank you for choosing [Temple Name]. It was our privilege to serve you in this spiritual journey.</p>
      
      <p>For any follow-up questions, please contact our office at <a href="mailto:poojai@temple.com">poojai@temple.com</a> or call +91 XXXXX XXXXX.</p>
      
      <p>With divine blessings,<br>The [Temple Name] Team</p>
      
      <a href="#" class="btn">Download Poojai Photos</a>
    </div>
    
    <div class="footer">
      <p>© 2023 {temple_name}. All rights reserved.</p>
      <p>Follow our spiritual activities: [Social Media Links]</p>
    </div>
  </div>
</body>
</html>"""


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
