#

# ?FastApi
from fastapi import APIRouter

# ?Models,Serializers and Manager class
from .auth import router


# Create APIRouter instance from APIRouter class
api_router = APIRouter()
api_router.include_router(router)
