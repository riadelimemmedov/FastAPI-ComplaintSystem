#

# ?FastApi
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, SecretStr, validator


# ?Third Party packages for FastApi
from email_validator import validate_email as validate_user_email, EmailNotValidError


# ?Pyhon modules and Functions
import re


#!UserBase
class UserBase(BaseModel):
    email: str

    # validate_email
    @validator("email")
    def validate_email(cls, email):
        try:
            validate_user_email(email)
            return email
        except EmailNotValidError:
            raise ValueError("Email is not valid format")


# *UserRegisterIn
class UserRegisterIn(UserBase):
    password: str
    phone: str
    first_name: str
    last_name: str
    full_name: str
    iban: str

    # validate_phone
    @validator("phone")
    def validate_phone(cls, phone):
        regex_pattern = "994\s?\d{2}[2-9]\d{6}"
        if re.match(regex_pattern, phone):
            return phone
        else:
            raise ValueError("Phone number must be in this format:994xxxxxxxxx'")

    # validate_full_name
    @validator("full_name")
    def validate_full_name(cls, full_name):
        try:
            first_name, last_name = full_name.split()
            return full_name
        except Exception as ex:
            raise ValueError("You should provide at least first_name and last_name")


# *UserLoginIn
class UserLoginIn(UserBase):
    password: str
