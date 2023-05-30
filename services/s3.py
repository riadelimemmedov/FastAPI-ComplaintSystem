#

# ?Python modules and function
import boto3
from decouple import config
from fastapi import Depends, FastAPI, HTTPException, Request, status


#!S3Service
class S3Service:
    def __init__(self):
        self.key = config("AWS_ACCSES_KEY")
        self.secret = config("AWS_SECRET_KEY")
        self.s3 = boto3.client(
            "s3", aws_access_key_id=self.key, aws_secret_access_key=self.secret
        )
        self.bucket = config("AWS_BUCKET_NAME")

    # upload
    def upload(self, path, key, extension):
        try:
            self.s3.upload_file(
                path,
                self.bucket,
                key,
                ExtraArgs={"ACL": "public-read", "ContentType": f"image/{extension}"},
            )
            return f"https://{self.bucket}.s3.amazonaws.com/{key}"
        except Exception as ex:
            raise HTTPException(500, "S3 is not available")


#
