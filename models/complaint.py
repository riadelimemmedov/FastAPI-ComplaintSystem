#

# ?FastApi
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, SecretStr, validator


# ?Third Party packages for FastApi
import sqlalchemy


# ? Models and Serializer class
from .enums import RoleType, State


# ?Database properties
from db import metadata


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
)
