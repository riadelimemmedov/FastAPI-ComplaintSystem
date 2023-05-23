#

# ?FastApi
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, SecretStr, validator


#!UserBase
class UserBase(BaseModel):
    email: str


# *UserRegisterIn
class UserRegisterIn(UserBase):
    password: str
    phone: str
    first_name: str
    last_name: str
    full_name: str
    iban: str


# *UserLoginIn
class UserLoginIn(UserBase):
    password: str
