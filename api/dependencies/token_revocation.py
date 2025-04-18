from security.jwt_token import JwtTokenVerification
from fastapi import Request,HTTPException


async def revoke(request:Request):
    try:
        token=request.headers.get("Authorization")
        if token:
            bearer,token=token.split(' ')
            if bearer!="Bearer":
                raise HTTPException(
                    status_code=422,
                    detail="invalid token format add bearer"
                )
            data={
                "user_agent":request.headers.get("User-Agent"),
                "accept_language":request.headers.get("Accept-Language")
            }
            return {"access_token":await JwtTokenVerification().get_new_access_token(refresh_token=token,data=data)}
        
        raise HTTPException(
            status_code=401,
            detail="token missing"
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"something went wrong on token verification {e}"
        )