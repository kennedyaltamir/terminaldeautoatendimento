# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-08 22:30:00
import os
import boto3
import uuid
import logging
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import UploadFile

logger = logging.getLogger("StorageService")

class StorageService:
    def __init__(self):
        self.provider = "local"
        self.bucket_name = os.getenv("AWS_BUCKET_NAME")
        self.region = os.getenv("AWS_REGION", "us-east-1")
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.endpoint_url = os.getenv("AWS_ENDPOINT_URL") # Para R2/MinIO

        if self.bucket_name and self.access_key and self.secret_key:
            self.provider = "s3"
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region,
                endpoint_url=self.endpoint_url
            )
            logger.info(f"StorageService inicializado: S3 ({self.bucket_name})")
        else:
            logger.info("StorageService inicializado: Local Filesystem")

    async def upload_file(self, file: UploadFile) -> str:
        """
        Faz upload do arquivo e retorna a URL pública.
        """
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        content_type = file.content_type

        if self.provider == "s3":
            return self._upload_s3(file.file, unique_filename, content_type)
        else:
            return await self._upload_local(file, unique_filename)

    def _upload_s3(self, file_obj, filename: str, content_type: str) -> str:
        try:
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                filename,
                ExtraArgs={'ContentType': content_type, 'ACL': 'public-read'}
            )
            
            # Constrói a URL
            if self.endpoint_url:
                # Ex: Cloudflare R2
                return f"{self.endpoint_url}/{self.bucket_name}/{filename}"
            else:
                # AWS S3 Padrão
                return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{filename}"

        except ClientError as e:
            logger.error(f"Erro S3: {e}")
            raise Exception("Falha no upload para nuvem")

    async def _upload_local(self, file: UploadFile, filename: str) -> str:
        try:
            upload_dir = "frontend/public/uploads"
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)
            
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            
            return f"/uploads/{filename}"
        except Exception as e:
            logger.error(f"Erro Local Storage: {e}")
            raise Exception("Falha no upload local")

# Instância Global
storage = StorageService()
