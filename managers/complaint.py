#

# ?Models,Serializers and Manager class
# ?Database
# ? Python function and modules
import os
import uuid

from decouple import config

from constants import TEMP_FILE_FOLDER
from db import database
from models import complaint, user
from models.enums import RoleType, State

# ?S3 and helpers methods for upload image to Cloud
from services.s3 import S3Service
from services.ses import SESService
from utils.helpers import decode_photo

# ?AuthManager
from .auth import AuthManager

# S3 instance
s3 = S3Service()
ses = SESService()


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
        encoded_photo = complaint_data["encoded_photo"]
        extension = complaint_data["extension"]
        name = f"{uuid.uuid4()}.{extension}"
        print("Name value is ", name)
        path = os.path.join(TEMP_FILE_FOLDER, name)  # uploadded image path
        print("Path value is ", path)
        decode_photo(path, encoded_photo)
        complaint_data["photo_url"] = s3.upload(path, name, extension)
        os.remove(path)
        id_ = await database.execute(complaint.insert().values(**complaint_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    # delete_complaint
    @staticmethod
    async def delete_complaint(complaint_id):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    # approve
    @staticmethod
    async def approve(complaint_id):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == complaint_id)
            .values(status=State.approved)
        )
        ses.send_email(
            "Complaint approved!",
            [config("RECEIVER")],
            "Congrats! Your claim is approved,check your bank account in 2 days for your refund",
        )

    # reject
    @staticmethod
    async def reject(complaint_id):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == complaint_id)
            .values(status=State.rejected)
        )
