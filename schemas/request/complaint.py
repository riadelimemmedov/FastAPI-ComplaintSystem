#

# ?FastApi
# ?Pyhon modules and Functions
import re

# ?Third Party packages for FastApi
from email_validator import EmailNotValidError
from email_validator import validate_email as validate_user_email
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, SecretStr, validator

# ?Models,Serializers,Schemas and Manager class
from models import complaint, user
from models.enums import RoleType, State
from schemas.base import BaseComplaint


# *ComplaintIn
class ComplaintIn(BaseComplaint):
    encoded_photo: str
    extension: str
