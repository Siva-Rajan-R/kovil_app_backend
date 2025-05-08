from pydantic import EmailStr
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