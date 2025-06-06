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
  "private_key_id": "6ab7a4b1a64d23a0f3666f85148cc88f635b38ee",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQChcPTam2Ekluj2\n/zSJgfYGRzMzULgF11ekAQnMtnUasi98d3M31UUkl8X0kFFqB9XpYseR40HCaxvy\nVUUA8/LsgTHh8H0F5QRo3FaP2W5iAi73zivP/hjTb4oVPRGTpcUm1pU8rv96Tl5o\nqzwClVaZJkhjm0N9Emx4gjdWFnC5d8UPx+GZQ17nOz+F81vXM4iPo/qvgHEVhiKS\n4XB7I2DFPL8G8ffZWHVvdRIXnPdZeY628DEmwBa6bm7wun5ZUzaJokszi+VhJQwU\nssVhrzXHOpKduQOAks5+ZAfeiBV1SVRgrCH4OCpm6WhJaBG07xPMuMmbcK9BL4bE\nGo4+8D5HAgMBAAECgf8YEZRvrbqjOdyBoTVeoCw4bg+0FtSuCkIxW/ZEuZm74Soz\nOZvJNy1Ccgjml/LgsUpdq9xqY6HqL7h66JDhE32kGkmAOy+92+b3EI0sj74P3pjM\nrnAvEjL2qCpuACzJVm2OMhpjHF6lCAoLO3w25mItcwetJ04TLNapy2rJ6uPjbTr0\n46NnzsHnxnhmESiYZurkJlPxuzVsSoJGIVi1+9Lzztm3iYJs+/il0IFbvjY++zaP\nABK+qqkgA/SvccHXwPTI2d+MvI0CdRAvEvD8mX6/El8kriQLRx0tyiWbGsaDNBYM\nJN3WrXkvs16+yNM+1G5zeGfuY2LpKoYIcqDyM8UCgYEA3QK0F9ZI2j0e6/pse9rO\nd38IZSvqCU/nOo0XbpsWrzxALdzQLxDCpWNeWOeym4q3UEUBEuYuIojBwrmVXbFL\ntNk+Y7qXDMZGSlZU6MHIofNNB3MMcOy1UMk0v2tC7bXEmha1YqbFEmoILr2tqsuG\n1rXWGL2ryaTBavsOEaRnDhMCgYEAuv/6jsWTsjAKJ+XToEtcCYIuy6kzAQH9RF9n\n8Q3nkYt0YynEmPZ2FZcHKg3UpamwoavAZmPaIk6tP4zGfcCMxIGc+gYxqACLiyMs\n87GDNLimUvJuTOGL8SSA8NYx1Dzdf5fKm6l3tWgmKAWpKTn5f2XMLH8CfMIWO/yq\nJQBIBX0CgYAG7vbHaKmQbypxLMIKgKrJhOq2gdItyJvwckyx45uqk7FPvwWo9FWm\n6p8jGuG3j3qAwiludlosKy4o9bmB3vYJDmeuqUPj2rSJ0HuJccrhich421sgj8yA\nZE+LUcofuvwX+W5nUeQM19a54Kl6Gjh4s+uriwfAo7KNsKKYWxgAkQKBgQCIJE7l\nXMDPrJvoOjGddN/36Dhre66vYCRkf9UrsUTTOKUugL0p491KkJ7dph4X0ffPbDxy\nDuZDreYB61qjOOkDM532hUXnmyX80UorzSPJ4Vjt8KQPAvIgSMQ7EqZKb1mPSBJw\ny6tkfgOxhZWHdzbG4nUIPBuyepc3axbwQ0kr/QKBgFscxt+BJqn8jIkl5AwQH8ND\niibtweclImMIdh4Cg41H6p9PRuTNiebPvQ1bvc9Pb1txQK4Pz15pE5P1heSS+FcL\ncWorWKTQ8X2HgE4mOWiJKoQ04RFxcFd+xhBHQuautts8h7x/10mcMJJ5QFrQX/wl\nSjtN49kTsebfX9tOSbcs\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@nanmaitharvuar-kovilapp.iam.gserviceaccount.com",
  "client_id": "116693207395193647208",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40nanmaitharvuar-kovilapp.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
print(json.dumps(data))