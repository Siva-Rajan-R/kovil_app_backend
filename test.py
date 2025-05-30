import os
print(os.urandom(64))

import secrets

# Generate a 256-bit random key (32 bytes) in hex
jwt_secret = secrets.token_urlsafe(64)
print(jwt_secret)

from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(key.decode())  # URL-safe base64-encoded 32-byte key
