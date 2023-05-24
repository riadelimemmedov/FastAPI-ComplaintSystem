#

# ?FastApi
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, SecretStr, validator


#!BaseComplaint
class BaseComplaint(BaseModel):
    title: str
    description: str
    photo_url: str
    amount: float
