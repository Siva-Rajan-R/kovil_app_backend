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

