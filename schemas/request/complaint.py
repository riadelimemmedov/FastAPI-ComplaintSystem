#

# ?FastApi
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, SecretStr, validator


# ?Third Party packages for FastApi
from email_validator import validate_email as validate_user_email, EmailNotValidError

# ?Pyhon modules and Functions
import re

# ?Models,Serializers,Schemas and Manager class
from models import user, complaint
from models.enums import RoleType, State
from schemas.base import BaseComplaint


# *ComplaintIn
class ComplaintIn(BaseComplaint):
    pass
