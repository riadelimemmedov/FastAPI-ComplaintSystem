
#?Models,Schemas and Serializers
from models import RoleType
from schemas.base import UserBase


#!UserOut
class UserOut(UserBase):
    id:int
    first_name : str
    last_name : str
    phone : str
    role : RoleType
    iban : str