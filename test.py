# import os
# print(os.urandom(64))

# import secrets

# # Generate a 256-bit random key (32 bytes) in hex
# jwt_secret = secrets.token_urlsafe(64)
# print(jwt_secret)

# from cryptography.fernet import Fernet

# key = Fernet.generate_key()
# print(key.decode())  # URL-safe base64-encoded 32-byte key

# import requests

# session = requests.Session()

# payload = {
#     "register_no": "911022104069",
#     "dob": "15-04-2005",
#     "security_code": "WT5M0Z",
#     "yo3d9X8Ij9Iw4H8Yg278": "yo3d9X8Ij9Iw4H8Yg278",
#     "gos":"Login"
# }
# url = "https://coe1.annauniv.edu/home/students_corner.php"
# # STEP 5: Submit the form
# post_response = session.post(url, data=payload,verify=False,cert=False)
# print(post_response.text)


# menus={
#     "idly":6,
#     "dosa":50,
#     "pongal":35
# }

# for item in menus.items():
#     print(f"{item[0]}-Rs {item[1]}")

# food=input("select a food name :")
# quantity=int(input("enter the food quantity :"))

# total_amount=quantity*(menus[food]+0.05)

# print(f"your food is : {food}\nquantity is : {quantity}\ntotal amount is : {total_amount}Rs")

"""import pyrebase

config=firebaseConfig = firebase_config = {
    "apiKey": "AIzaSyDfQB7WFMOj4xy4efWAWhKTJT2D-3jDPmY",
    "authDomain": "nanmaitharvuar-kovilapp.firebaseapp.com",
    "databaseURL": "https://nanmaitharvuar-kovilapp-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "nanmaitharvuar-kovilapp",
    "storageBucket": "nanmaitharvuar-kovilapp.appspot.com",
    "messagingSenderId": "424295283811",
    "appId": "1:424295283811:web:3c5c0ea86136d28f4a4c56",
    "measurementId": "G-77RXRTCNE6"
}

firebase_init=pyrebase.initialize_app(config=config)

from pydantic import EmailStr
from firebase_db.firebase_init import firebase_init
db=firebase_init.database()


# value=db.child("users_fcm_tokens").child("9677639292").get().val()
# value.append("new val")
# print(value,type(value))
h=db.child("users_fcm_tokens").child("9677639292")
h.set(["ko","lop"])"""

import json
data={
  "type": "service_account",
  "project_id": "nanmaitharvuar-kovilapp",
  "private_key_id": "e4acbcd4807257ba8c99450de91a8cd580cc7c02",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDOMfnN1fslWQYU\nznjGrKf5yFIPa91M7VXw+8wso9COQ/qPDqDs8igN16y8JvKO6KVVCjDtpn5v4z30\nHYr+BtddTH3jeEx1cpJ5ytOgZMEsSb69jFvJUsHCY4WR1GDU1xrUMlPF+9n09qRw\nhJyAmYC5uXwK6f9419if6ZeWDXRzRV1kotOK0c3bvhf2dPCRPLnNZZXDzy4Pl+DR\nTu3hMECRlioQN22FvDevrYqo4MJ0FqZkQz2g5Zzx3Izha411kYdNI5F4gevrmb/h\n+Xe5e5FYfTw8wuoX1zUDrwPyeE0OJrxLJPpvl83m9e6avg5ipsyzphaKoaDPBKxi\naK8kuAyjAgMBAAECggEAMhXDlvMGKSFBr+YjQicIOk0lWaeavqfbu0h+ZM15yETM\n5Njp0ARWJF6iD6XqPzpVhp2OGvvZNHZfQx+19lRVFc2RuqIq+FBXMgxJcWln3ske\n8s3YMcPPWtdvx2duCeUiGC8NWEb/v1f1w3sCxN4EfZiHf+Ms8f6EGPvVnVYxVhow\ncDez7eMwFrUblXbl5OmRen6e9Xltxt4YN7xcoW2QtI0s/xQ3uFXnbal9enL4MV5/\nNdFEhgBg4Kh17PvxPzLTn8LI8ifBaDdZI8ZyreFZxFdGQBFZu2MEawEulz6LXebx\nzJKsERLNWHtmL4BWl6aKjWjJZBrE8CfbTAKaSjFfAQKBgQDz0v+rqmNBtiwTixFM\nDDp/Z7k5D0Jz0e5+8pKRAgqyiJsGf2Db6CNvb545+e5+U9Itl25SRtiu8G13PODz\n5m09XAx5j7nlOrR/9DqXQZA1QCes77Hx66FskViWKjzuyXUdbrDzC/oh8jnP26Js\ncSsetvLnBk9WijQfIB2+JFiggQKBgQDYfe9xkXx9i+jJsnH7RAhI1laLXztJhX/X\nt6YNTeFRulhGDmoaWNKZRG9ud5ZBCHCXBzMWLBdmkT6bFELXQuHsd5asBSM/N7W9\nUEA6eIetPy+ttJrWrekkYjsAHbwO1cZ7onCkOBoJ4glIuHlWZJuZFQJ0QCZWw+jL\nl7gETWybIwKBgBsnvcfdsy5HXsNScru4hO9Zmvxq4ajKkbhbxc0WoCBgLHvdxejY\nAtJPaRzl5BT3uunO+r95GnrpVhe4lQk0+aeiz9TeGAMata2mgrwD1k7H9WNCUtwx\ntQnFaktXKvAhScTcZiK7i8EqHBw1RvKy6+2AzK7EOiPWQpXQ2t8pZyGBAoGAT95W\nIf3cgazGGvM8XciBje2VTCG8C6m2umzEVBAxWid3PZE/z6yJNYYr3gM8aY2li/Ja\nBIoLsAlRoYDeD/BazRRpf9j9Yes5nzgmGewxkdbHzjvdC+ppIsUioy5VHNv9N8t7\n5vnTkWXUqwFzsk23ochAeYbZHhV0ove8KcoukSUCgYB74BVoq4Mspgcd1jp0Q7RC\nMM36jnX5WLiAYipgDroB/czSg96M/AURr4HyoPvdCtwYRexJHJ1sSkMgewXBBJWD\nKpYnpB0ChxgE5Pn8V/lkJKNWrtpCApUhKJiwijPmMUVJaSLV8IOUX+lDJgSEbC9k\nYcBcyQ+Vg79XbHL7sSuTSQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@nanmaitharvuar-kovilapp.iam.gserviceaccount.com",
  "client_id": "116693207395193647208",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40nanmaitharvuar-kovilapp.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
print(json.dumps(data))