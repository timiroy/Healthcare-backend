import logging


from aiobotocore.session import get_session
from fastapi import UploadFile

from ai_health.root.settings import Settings
from ai_health.schemas.auth_schemas import User
from ai_health.schemas.file_upload_schema import UploadTarget

settings = Settings()

ACCESS_KEY = settings.AWS_ACCESS_KEY
SECRET_KEY = settings.AWS_SECRET_KEY
REGION = settings.AWS_REGION
BUCKET = settings.BUCKET_NAME
CLOUD_FRONT_URL = settings.CLOUD_FRONT_URL

LOGGER = logging.getLogger(__name__)


async def upload_file(file: UploadFile, upload_target: UploadTarget, user: User) -> (bool, str):
    session = get_session()
    async with session.create_client(
        "s3",
        region_name=REGION,
        aws_secret_access_key=SECRET_KEY,
        aws_access_key_id=ACCESS_KEY,
    ) as client:

        if upload_target == UploadTarget.PROFILE_IMAGE:
            file_key = f"PROFILE_IMAGE/{user.user_id}/{file.filename}"

        elif upload_target == UploadTarget.TEAM_MEMBER_IMAGE:
            file_key = f"TEAM_MEMBER_IMAGE/{file.filename}"

        elif upload_target == UploadTarget.COMPANY_LOGO:
            file_key = f"COMPANY_LOGO/{file.filename}"

        elif upload_target == UploadTarget.DOCUMENT:
            file_key = f"DOCUMENT/{file.filename}"

        else:
            file_key = f"FILE/{file.filename}"

        file_upload_response = await client.put_object(Bucket=BUCKET, Key=file_key, Body=file.file)

        if file_upload_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            file_link = f"{CLOUD_FRONT_URL}{file_key}"

            LOGGER.info(f"File uploaded path : {file_link}")
            print(f"File uploaded path : {file_link}")
            return (True, file_link)
    return False, ""
