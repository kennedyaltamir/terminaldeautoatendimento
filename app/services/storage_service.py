# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-02-05 02:45:00
import os
import boto3
import uuid
import logging
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import UploadFile
from dotenv import load_dotenv

# 🛡️ Hardening: Garante que variáveis locais sejam lidas em qualquer contexto de execução
load_dotenv()

logger = logging.getLogger("StorageService")

class StorageService:
    def __init__(self):
        self.provider = "local"
        self.bucket_name = os.getenv("AWS_BUCKET_NAME")
        self.region = os.getenv("AWS_REGION", "us-east-1")
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.endpoint_url = os.getenv("AWS_ENDPOINT_URL")

        if self.bucket_name and self.access_key and self.secret_key:
            try:
                client_kwargs = {
                    'service_name': 's3',
                    'aws_access_key_id': self.access_key,
                    'aws_secret_access_key': self.secret_key,
                    'region_name': self.region
                }
                if self.endpoint_url and str(self.endpoint_url).strip():
                    client_kwargs['endpoint_url'] = self.endpoint_url

                self.s3_client = boto3.client(**client_kwargs)
                self.provider = "s3"
                logger.info(f"✅ StorageService operacional: S3 ({self.bucket_name})")
            except Exception as e:
                logger.error(f"⚠️ Erro S3 (Fallback para Local): {e}")
                self.provider = "local"
        else:
            self.provider = "local"

    async def upload_file(self, file: UploadFile) -> str:
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        if self.provider == "s3":
            return self._upload_s3(file.file, unique_filename, file.content_type)
        return await self._upload_local(file, unique_filename)

    def _upload_s3(self, file_obj, filename, content_type):
        try:
            self.s3_client.upload_fileobj(
                file_obj, self.bucket_name, filename,
                ExtraArgs={'ContentType': content_type, 'ACL': 'public-read'}
            )
            return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{filename}"
        except Exception as e:
            logger.error(f"Erro upload S3: {e}")
            raise Exception("Falha no armazenamento em nuvem")

    async def _upload_local(self, file, filename):
        upload_dir = "frontend/public/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)
        await file.seek(0)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return f"/uploads/{filename}"

storage = StorageService()