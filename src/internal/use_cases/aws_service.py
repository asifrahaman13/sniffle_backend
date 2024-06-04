

from typing import Any
from src.infastructure.repositories.aws_repository import AWSRepository
from src.internal.interfaces.aws_interface import AWSInterface

class AwsService:
    def __call__(self) -> AWSInterface:
        return self

    def __init__(self, aws_repository= AWSRepository) -> None:
        self.aws_repository = aws_repository

    def upload_json(self, file_name: str, file_content: Any) -> bool:
        return self.aws_repository.upload_json(file_name, file_content)
    
    def get_presigned_json_url(self, file_name: str) -> str:
        return self.aws_repository.get_presigned_json_url(file_name)
    
