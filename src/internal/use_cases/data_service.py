from src.internal.interfaces.data_interface import DataInterface
from src.infastructure.repositories.database_repository import DatabaseRepository
import logging

class DataService:

    def __call__(self) -> DataInterface:
        return self
    
    def __init__(self):
        self.database_repository = DatabaseRepository()


    def get_general_metrics(self, user):
        try:

            # Get the general metrics for the user
            general_metrics = self.database_repository.find_single_document("email", user, "general_metrics")


            # Return the general metrics
            return general_metrics
        except Exception as e:
            logging.error(f"Failed to get general metrics: {e}")