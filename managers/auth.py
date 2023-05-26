#

# ?FastApi
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, SecretStr, validator


# ?Third Party packages for FastApi
import jwt
from decouple import config


# ?Pyhon modules and Functions
from datetime import datetime, timedelta
from typing import Optional


# ?Models,Serializers,Schemas and Manager class
from models.user import user
from models import user, complaint
from models.enums import RoleType, State
from schemas.base import BaseComplaint


# ?Database properties
from db import metadata, database


#!AuthManager
class AuthManager:
    @staticmethod
    def encode_token(user):
        try:
            payload = {
                "sub": user["id"],
                "exp": datetime.utcnow() + timedelta(minutes=120),
            }
            return jwt.encode(payload, config("JWT_SECRET"), algorithm="HS256")
        except Exception as ex:
            raise ex


#!CustomHTTPBearer
class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(
                res.credentials, config("JWT_SECRET"), algorithms=["HS256"]
            )
            user_data = await database.fetch_one(
                user.select().where(user.c.id == payload["sub"])
            )
            request.state.user = user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid token")


oauth2_schema = CustomHTTPBearer()


#!is_complainer
def is_complainer(request: Request):
    if not request.state.user["role"] == RoleType.complainer:
        raise HTTPException(403, "Forbidden")


#!is_approver
def is_approver(request: Request):
    if not request.state.user["role"] == RoleType.approver:
        raise HTTPException(403, "Forbidden")


#!is_admin
def is_admin(request: Request):
    if not request.state.user["role"] == RoleType.admin:
        raise HTTPException(403, "Forbidden")
