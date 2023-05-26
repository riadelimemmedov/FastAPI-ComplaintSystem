#

# ?FastApi
from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, SecretStr, validator

from managers.auth import is_admin, is_approver, is_complainer, oauth2_schema
from managers.complaint import ComplaintManager

# ?Schemas,Models,Manager
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut

# De


# router
router = APIRouter(tags=["Complaints"])


#!get_complaints
@router.get(
    "/complaints/",
    dependencies=[Depends(oauth2_schema)],
    response_model=List[ComplaintOut],
    status_code=200,
)
async def get_complaints(request: Request):
    user = request.state.user
    return await ComplaintManager.get_complaints(user)


#!create_complaint
@router.post(
    "/complaints/",
    dependencies=[Depends(oauth2_schema), Depends(is_complainer)],
    response_model=ComplaintOut,
    status_code=201,
)
async def create_complaint(request: Request, complaint: ComplaintIn):
    user = request.state.user
    return await ComplaintManager.create_complaint(complaint.dict(), user)


#!delete_complaint
@router.delete(
    "/complaints/{complaint_id}/",
    dependencies=[Depends(oauth2_schema), Depends(is_admin)],
    status_code=204,
)
async def delete_complaint(complaint_id: int):
    await ComplaintManager.delete_complaint(complaint_id)


#!approve_complaint
@router.put(
    "/complaints/{complaint_id}/approve/",
    dependencies=[Depends(oauth2_schema), Depends(is_approver)],
    status_code=204,
)
async def approve_complaint(complaint_id: int):
    await ComplaintManager.approve(complaint_id)


#!approve_complaint
@router.put(
    "/complaints/{complaint_id}/reject/",
    dependencies=[Depends(oauth2_schema), Depends(is_approver)],
    status_code=204,
)
async def reject_complaint(complaint_id: int):
    await ComplaintManager.reject(complaint_id)
