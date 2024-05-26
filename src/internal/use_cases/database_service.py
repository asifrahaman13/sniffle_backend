from src.internal.interfaces.database_interface import DatabaseInterface
from src.infastructure.repositories.database_repository import DatabaseRepository


class DatabaseService:

    def __call__(self) -> DatabaseInterface:
        return self

    def __init__(self, database_repository=DatabaseRepository):
        self.database_repository = database_repository
    
    def find_one(self, field: str, field_value: str, collection_name: str):
        return self.database_repository.find_single_document(field, field_value, collection_name)
    
    def insert_one(self, data: str, collection_name: str):
        return self.database_repository.insert_single_document(data, collection_name)
    
