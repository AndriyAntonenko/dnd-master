import aioboto3
from botocore.exceptions import ClientError

from app.core.config import settings


class FilesStorageService:
    def __init__(self):
        self.session = aioboto3.Session()
        self.bucket = settings.DO_SPACES_BUCKET
        self.region = settings.DO_SPACES_REGION
        self.config = {
            "region_name": settings.DO_SPACES_REGION,
            "endpoint_url": settings.DO_SPACES_ENDPOINT,
            "aws_access_key_id": settings.DO_SPACES_KEY,
            "aws_secret_access_key": settings.DO_SPACES_SECRET,
        }

    async def upload_file(self, file_content, file_name, content_type) -> str:
        try:
            async with self.session.client("s3", **self.config) as client:
                await client.put_object(
                    Bucket=self.bucket,
                    Key=file_name,
                    Body=file_content,
                    ACL="public-read",
                    ContentType=content_type,
                )

            url = f"https://{self.bucket}.{self.region}.cdn.digitaloceanspaces.com/{self.bucket}/{file_name}"
            return url
        except ClientError as e:
            print(f"Error uploading file: {e}")
            return None

    async def delete_file(self, file_name):
        try:
            async with self.session.client("s3", **self.config) as client:
                await client.delete_object(Bucket=self.bucket, Key=file_name)
            return True
        except ClientError as e:
            print(f"Error deleting file: {e}")
            return False
