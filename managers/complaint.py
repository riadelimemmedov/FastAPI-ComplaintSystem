#

# ?Models,Serializers and Manager class
# ?Database
# ? Python function and modules
import os
import uuid

from decouple import config

from constants import TEMP_FILE_FOLDER
from db import database
from models import complaint, transaction, user
from models.enums import RoleType, State

# ?S3 and helpers methods for upload image to Cloud
from services.s3 import S3Service
from services.ses import SESService
from services.wise import WiseService
from utils.helpers import decode_photo

# ?AuthManager
from .auth import AuthManager

# Services
s3 = S3Service()
ses = SESService()
wise = WiseService() 


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
        data = complaint_data
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

        async with database.transaction() as tconn:
            id_ = await tconn._connection.execute(
                complaint.insert().values(**complaint_data)
            )

            await ComplaintManager.issue_transaction(
                tconn,
                data["amount"],
                f"{user['first_name']} {user['last_name']}",
                user["iban"],
                id_,
            )
            return await database.fetch_one(
                complaint.select().where(complaint.c.id == id_)
            )

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
        transaction_data = await database.fetch_one(
            transaction.select().where(transaction.c.complaint_id == complaint_id)
        )
        wise.fund_transfer(transaction_data["transfer_id"])
        ses.send_email(
            "Complaint approved!",
            [config("RECEIVER")],
            "Congrats! Your claim is approved,check your bank account in 2 days for your refund",
        )

    # rejectf
    @staticmethod
    async def reject(complaint_id):
        transaction_data = await database.fetch_one(
            transaction.select().where(transaction.c.complaint_id == complaint_id)
        )
        wise.cancel_transfer(transaction_data["transfer_id"])
        await database.execute(
            complaint.update()
            .where(complaint.c.id == complaint_id)
            .values(status=State.rejected)
        )

    # issue_transaction
    @staticmethod
    async def issue_transaction(tconn, amount, full_name, iban, complaint_id):
        quote_id = wise.create_quote(amount)
        recepient_id = wise.create_recipient_account(full_name, iban)
        transfer_id = wise.create_transfer(recepient_id, quote_id)
        data = {
            "quote_id": quote_id,
            "transfer_id": transfer_id,
            "target_account_id": str(recepient_id),
            "amount": amount,
            "complaint_id": complaint_id,
        }
        await tconn._connection.execute(transaction.insert().values(**data))
