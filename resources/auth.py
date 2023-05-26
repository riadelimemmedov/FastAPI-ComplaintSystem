#

# ?FastApi
from fastapi import APIRouter


# ?Models,Serializers and Manager class
from managers.user import UserManager


# ?Schemas
from schemas.request.user import UserRegisterIn, UserLoginIn


# router
router = APIRouter(tags=["Auth"])


#!register
@router.post("/register/", status_code=201)
async def register(user_data: UserRegisterIn):
    token = await UserManager.register(user_data.dict())
    return {"token": token}


#!login
@router.post("/login/", status_code=200)
async def login(user_data: UserLoginIn):
    token = await UserManager.login(user_data.dict())
    return {"token": token}
