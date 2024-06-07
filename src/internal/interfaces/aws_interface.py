from abc import ABC, abstractmethod
from typing import Any


class AWSInterface(ABC):

    @abstractmethod
    def upload_json(self, file_name: str, file_content: Any) -> None:
        """Upload a JSON file with the specified name and content."""
        pass

    @abstractmethod
    def get_presigned_json_url(self, file_name: str) -> str:
        """Get a presigned URL for the specified JSON file."""
        pass
