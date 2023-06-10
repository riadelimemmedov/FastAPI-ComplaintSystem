#

# ?FastApi
# ?Third Party packages for FastApi
from email_validator import EmailNotValidError
from email_validator import validate_email as validate_user_email
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, SecretStr, validator

import re

#!BaseComplaint
class BaseComplaint(BaseModel):
    title: str
    description: str
    amount: float


#!UserBase
class UserBase(BaseModel):
    email: str

    # validate_email
    @validator("email")  
    def validate_email(cls, email):
        try:
            pattern = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
            return re.match(pattern,email) is not None
        except EmailNotValidError:
            raise ValueError("Email is not valid format")
