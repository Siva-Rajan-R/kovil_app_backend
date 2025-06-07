from firebase_db.firebase_init import firebase_init
from icecream import ic
from fastapi.exceptions import HTTPException
class FirebaseCrud:

    def __init__(self,user_id:str):
        self.db=firebase_init.database()
        self.user_id=user_id

    def add_fcm_tokens(self,fcm_token:str,device_id:str):
        try:
            self.db.child("users_fcm_tokens").child(self.user_id).child("devices").child(device_id).set(fcm_token)

            return "successfully added fcm token"
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while adding fcm token {e}"
            )
    
    def get_fcm_tokens(self):
        try:
            return self.db.child("users_fcm_tokens").child(self.user_id).child("devices").get().val()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while getting fcm token {e}"
            )
    
    def delete_fcm_token(self,device_id):
        try:
            ic(self.user_id)
            self.db.child("users_fcm_tokens").child(self.user_id).child("devices").child(device_id).remove()
            return "removed token successfully"
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while deleting fcm token {e}"
            )
