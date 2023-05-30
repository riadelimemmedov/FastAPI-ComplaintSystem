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

#!Complaint
complaint = sqlalchemy.Table(
    "complaints",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(120), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("photo_url", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column(
        "created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()
    ),
    sqlalchemy.Column(
        "status", sqlalchemy.Enum(State), server_default=State.pending.name
    ),
    sqlalchemy.Column(
        "complainer_id", sqlalchemy.ForeignKey("users.id"), nullable=False
    ),
    sqlalchemy.Column("encoded_photo", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column(
        "extension", sqlalchemy.String(100), nullable=False, server_default="jpeg"
    ),
)
