#

# ?FastApi
# ?Pyhon modules and Functions
import enum
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, SecretStr, validator

from managers.auth import is_admin, is_complainer, oauth2_schema
from managers.complaint import ComplaintManager
from managers.user import UserManager
from models import RoleType
# ?Schemas,Models,Manager
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut
from schemas.response.user import UserOut

# router
router = APIRouter(tags=["Users"])


#!get_all_users
@router.get("/users/", dependencies=[Depends(oauth2_schema), Depends(is_admin)],response_model=List[UserOut],status_code=200)
async def get_all_users(email: Optional[str] = None):
    if email:
        return await UserManager.get_user_by_email(email)
    return await UserManager.get_all_users()


#!make_admin
@router.put('/users/{user_id}/make-admin',dependencies=[Depends(oauth2_schema),Depends(is_admin)],status_code=204)
async def make_admin(user_id:int):
    await UserManager.change_role(RoleType.admin,user_id)


#!make_approver
@router.put('/users/{user_id}/make-approver',dependencies=[Depends(oauth2_schema),Depends(is_admin)],status_code=204)
async def make_approver(user_id:int):
    await UserManager.change_role(RoleType.approver,user_id)