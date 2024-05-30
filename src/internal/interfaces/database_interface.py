from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
    @abstractmethod
    def find_one(self, field: str, field_value: str, collection_name: str):
        pass

    @abstractmethod
    def insert_one(self, data: str, collection_name: str):
        pass
