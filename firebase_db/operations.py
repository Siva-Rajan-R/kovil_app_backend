from firebase_db.firebase_init import firebase_init
from icecream import ic
class FirebaseCrud:

    def __init__(self,user_mobile_number:str):
        self.db=firebase_init.database()
        self.user_mobile_number=user_mobile_number

    def add_fcm_tokens(self,fcm_token:str):
        query_value=self.get_fcm_tokens()

        if query_value:
            query_value.append(fcm_token)
        else:
            query_value=[fcm_token]

        self.db.child("users_fcm_tokens").child(self.user_mobile_number).set(query_value)

        return "successfully added fcm token"
    
    def get_fcm_tokens(self):
        return self.db.child("users_fcm_tokens").child(self.user_mobile_number).get().val()
