"""S3/MinIO storage utilities."""
import boto3
import json
from typing import Any, Dict
from src.config import get_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class StorageClient:
    """S3/MinIO storage client."""
    
    def __init__(self):
        self.endpoint_url = f"http://{get_config('s3', 'endpoint')}"
        self.access_key = get_config('s3', 'access_key')
        self.secret_key = get_config('s3', 'secret_key')
        
