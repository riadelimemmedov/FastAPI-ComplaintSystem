#

# ?FastApi
# ?Third Party packages for FastApi
import sqlalchemy
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, SecretStr, validator

# ?Database properties
from db import metadata

# ? Models and Serializer class
from .enums import RoleType, State

#!User
user = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(120), unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(255)),
    sqlalchemy.Column("first_name", sqlalchemy.String(200)),
    sqlalchemy.Column("last_name", sqlalchemy.String(200)),
    sqlalchemy.Column("full_name", sqlalchemy.String(200)),
    sqlalchemy.Column("phone", sqlalchemy.String(200)),
    sqlalchemy.Column(
        "role",
        sqlalchemy.Enum(RoleType),
        nullable=False,
        server_default=RoleType.complainer.name,
    ),
    sqlalchemy.Column("iban", sqlalchemy.String(200)),
)
