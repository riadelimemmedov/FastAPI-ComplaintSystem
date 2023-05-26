#

# ?FastApi
from asyncpg import UniqueViolationError
from fastapi import FastAPI, HTTPException

# ?Third Party packages for FastApi
from passlib.context import CryptContext

# ?Database
from db import database

# ?Models,Serializers and Manager class
from models import RoleType, user

from .auth import AuthManager

# pwd_context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#!UserManager
class UserManager:
    # register
    @staticmethod
    async def register(user_data):
        user_data["password"] = pwd_context.hash(user_data["password"])
        try:
            id_ = await database.execute(user.insert().values(**user_data))
            print("User id is ", id_)
        except UniqueViolationError:
            raise HTTPException(400, "User with this email already exists")
        created_user = await database.fetch_one(user.select().where(user.c.id == id_))
        return AuthManager.encode_token(created_user)

    # login
    @staticmethod
    async def login(user_data):
        user_do = await database.fetch_one(
            user.select().where(user.c.email == user_data["email"])
        )
        if not user_do:
            raise HTTPException(400, "Wrong email or password")
        elif not pwd_context.verify(user_data["password"], user_do["password"]):
            raise HTTPException(400, "Wrong email or password")
        return AuthManager.encode_token(user_do)

    # get_all_users
    @staticmethod
    async def get_all_users():
        return await database.fetch_all(user.select())

    # get_user_by_email
    @staticmethod
    async def get_user_by_email(email):
        return await database.fetch_all(user.select().where(user.c.email == email))

    @staticmethod
    async def change_role(role: RoleType, user_id):
        existing_user = await database.fetch_one(
            user.select().where(user.c.id == user_id)
        )
        print("Existing user is ", existing_user.role)
        if existing_user.role != "admin":
            await database.execute(
                user.update().where(user.c.id == user_id).values(role=role)
            )
