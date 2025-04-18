from pydantic import EmailStr

def not_found():
    return """
    <body style="min-height: 100vh; display: flex; justify-content: center; align-items: center; background-color: #000435; margin: 0;">
        <div style="background-color: #ff4c4c; padding: 30px; border-radius: 8px; text-align: center; max-width: 400px;">
            <h1 style="color: white; font-size: 24px;">Error 404</h1>
            <p style="color: white; font-size: 16px; margin-top: 10px;">Page Not Found or Request Timed Out</p>
        </div>
    </body>
    """

def register_accept_greet(name:str,email:EmailStr,number:str):
    return f"""
            <html>
            <body>
            <div style="min-height: 100vh; display: flex; justify-content: center; align-items: center; width: 100%; background: #000435;">
            <div style="background: #000435; max-width: 600px; border-radius: 8px; padding: 40px 32px; text-align: center; box-shadow: 0 0 20px rgba(52, 224, 247, 0.2);">
                <!-- Animated Checkmark -->
                <div style="width: 80px; height: 80px; background: #4BB543; border-radius: 50%; margin: 0 auto 30px; display: flex; align-items: center; justify-content: center; animation: checkmark-anim 0.6s ease-in-out;">
                <svg style="width: 40px; height: 40px; fill: white;" viewBox="0 0 24 24">
                    <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                </svg>
                </div>

                <!-- Success Message -->
                <h2 style="color: #34e0f7; font-size: 28px; margin-bottom: 15px;">
                Registration Accepted Successfully!
                </h2>
                
                <!-- Admin-specific Text -->
                <div style="color: white; font-size: 16px; line-height: 1.6; margin-bottom: 30px;">
                <p>You have approved the registration for:</p>
                <div style="margin: 20px 0;">
                    <div style="margin-bottom: 10px;">
                    <span style="color: #34e0f7;">Name: </span>
                    <strong style="color: white;">{name}</strong>
                    </div>
                    <div>
                    <span style="color: #34e0f7;">Email: </span>
                    <strong style="color: white;">{email}</strong>
                    </div>
                    <div>
                    <span style="color: #34e0f7;">Mobile Number: </span>
                    <strong style="color: white;">{number}</strong>
                    </div>
                </div>
                </div>
            </div>
            </div>
            </body>
            </html>
    """

def forgot_accept_greet(email_or_no:EmailStr|str):
    return f"""
            <html>
            <body>
            <div style="min-height: 100vh; display: flex; justify-content: center; align-items: center; width: 100%; background: #000435;">
            <div style="background: #000435; max-width: 600px; border-radius: 8px; padding: 40px 32px; text-align: center; box-shadow: 0 0 20px rgba(52, 224, 247, 0.2);">
                <!-- Animated Checkmark -->
                <div style="width: 80px; height: 80px; background: #4BB543; border-radius: 50%; margin: 0 auto 30px; display: flex; align-items: center; justify-content: center; animation: checkmark-anim 0.6s ease-in-out;">
                <svg style="width: 40px; height: 40px; fill: white;" viewBox="0 0 24 24">
                    <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                </svg>
                </div>

                <!-- Success Message -->
                <h2 style="color: #34e0f7; font-size: 28px; margin-bottom: 15px;">
                Forgot Credentials Accepted Successfully!
                </h2>
                
                <!-- Admin-specific Text -->
                <div style="color: white; font-size: 16px; line-height: 1.6; margin-bottom: 30px;">
                <p>You have approved the forgot cred for:</p>
                <div style="margin: 20px 0;">
                    <div style="margin-bottom: 10px;">
                    <span style="color: #34e0f7;">Email or Mobile Number: </span>
                    <strong style="color: white;">{email_or_no}</strong>
                    </div>
                </div>
                </div>
            </div>
            </div>
            </body>
            </html>
    """
