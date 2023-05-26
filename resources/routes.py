#

# ?FastApi
from fastapi import APIRouter

# ?Models,Serializers and Manager class
from resources import auth, complaint, user

# Create APIRouter instance from APIRouter class
api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(complaint.router)
api_router.include_router(user.router)

# comment
# user url
