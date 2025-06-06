import pyrebase
import os,json
from dotenv import load_dotenv
load_dotenv()

config=json.loads(os.getenv("FIREBASE_CONFIG"))

print(type(config))
firebase_init=pyrebase.initialize_app(config=config)


