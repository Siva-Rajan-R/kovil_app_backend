from fastapi import APIRouter
import os
import json
from dotenv import load_dotenv
load_dotenv()


router=APIRouter(
    tags=["get the current version"]
)

version_info=os.getenv("VERSION_INFO")

@router.get("/app/version")
def get_app_version():
    return json.loads(version_info)