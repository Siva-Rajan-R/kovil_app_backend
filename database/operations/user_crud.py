from database.models.user import Users,UserRole
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from database.operations.user_auth import UserVerification
from enums import backend_enums
from icecream import ic

class __UserDeleteInputs:
    def __init__(self,session:Session,user_id:str,del_user_id:str):
        self.session=session
        self.user_id=user_id
        self.del_user_id=del_user_id

class DeleteUser(__UserDeleteInputs):
    async def delete_user(self):
        
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                ic(user.role)
                if user.role==UserRole.ADMIN:
                    is_deleted=self.session.query(Users).filter(Users.id==self.del_user_id).delete()
                    if is_deleted:
                        return "user deleted successfully"
                    raise HTTPException(
                        status_code=404,
                        detail="user doesn't exists"
                    )
                raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to make any changes"
                )
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while deleting user {e}"
            )


class GetUsers:
    def __init__(self,session:Session,user_id:str):
        self.session=session
        self.user_id=user_id

    async def get_users(self):
        try:
            user=await UserVerification(session=self.session).is_user_exists_by_id(id=self.user_id)
            if user.role==UserRole.ADMIN:
                users=self.session.execute(
                    select(
                        Users.id,
                        Users.name,
                        Users.email,
                        Users.mobile_number,
                        Users.role
                    )
                ).mappings().all()

                ic({"users":users})
                return {"users":users}
            raise HTTPException(
                    status_code=401,
                    detail="you are not allowed to get this information"
                )
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while fetching users {e}"
            )
        
class UpdateUser:
    def __init__(self,session:Session,user_id:str):
        self.session=session
        self.user_id=user_id

    async def update_user_role(self,user_id_to_update:str,role_to_update:backend_enums.UserRole):
        try:
            with self.session.begin():
                user=await UserVerification(session=self.session).is_user_exists_by_id(self.user_id)
                if user.role==backend_enums.UserRole.ADMIN:
                    self.session.query(Users).filter(Users.id==user_id_to_update).update(
                        {
                            Users.role:role_to_update
                        }
                    )

                    return "user role updated successfully"
                else:
                    raise HTTPException(
                        status_code=401,
                        detail="you are not allowed to make any changes"
                    )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong while updating user role {e}"
            )