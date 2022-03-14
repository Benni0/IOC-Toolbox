import os
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer

#API_KEYS = os.getenv('API_KEY').split(",")
API_KEYS = "hugo,hugine".split(",")

security = HTTPBearer()

def check_api_key(auth_data: HTTPBearer = Depends(security)):
    if not auth_data.credentials in API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return True