#

# ?FastApi
from typing import List
from fastapi import APIRouter
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, SecretStr, validator

# ?Schemas,Models,Manager
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut
from managers.auth import oauth2_schema, is_complainer, is_admin
from managers.complaint import ComplaintManager
from managers.user import UserManager


# ?Pyhon modules and Functions
import enum
from datetime import datetime, timedelta
from typing import Optional


# router
router = APIRouter(tags=["Users"])


#!get_all_users
@router.get("/users/", dependencies=[Depends(oauth2_schema), Depends(is_admin)])
async def get_all_users(email: Optional[str] = None):
    if email:
        return await UserManager.get_user_by_email(email)
    return await UserManager.get_all_users()
