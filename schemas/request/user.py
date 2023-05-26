#

# ?FastApi
# ?Pyhon modules and Functions
import re

from email_validator import EmailNotValidError
from email_validator import validate_email as validate_user_email
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, SecretStr, validator

from schemas.base import UserBase


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
