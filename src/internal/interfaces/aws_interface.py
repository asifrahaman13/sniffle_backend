from abc import ABC, abstractmethod

class AWSInterface(ABC):
    @abstractmethod
    def upload_json(self, file_name, file_content):
        pass

    @abstractmethod
    def get_presigned_json_url(self, file_name):
        pass