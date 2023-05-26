#

# ?Models,Serializers and Manager class
# ?Database
from db import database
from models import complaint, user
from models.enums import RoleType, State

from .auth import AuthManager


#!ComplaintManager
class ComplaintManager:
    # get_complaints
    @staticmethod
    async def get_complaints(user):
        qs = complaint.select()
        if user["role"] == RoleType.complainer:
            qs = qs.where(complaint.c.complainer_id == user["id"])
        elif user["role"] == RoleType.approver:
            qs = qs.where(complaint.c.state == State.pending)
        return await database.fetch_all(qs)

    # create_complaint
    @staticmethod
    async def create_complaint(complaint_data, user):
        complaint_data["complainer_id"] = user["id"]
        id_ = await database.execute(complaint.insert().values(**complaint_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    # delete_complaint
    @staticmethod
    async def delete_complaint(complaint_id):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    
    