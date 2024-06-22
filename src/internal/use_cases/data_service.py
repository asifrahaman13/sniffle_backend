from concurrent.futures import ThreadPoolExecutor
from src.internal.interfaces.data_interface import DataInterface
from src.infastructure.repositories.database_repository import (
    DatabaseRepository,
)
from src.infastructure.repositories.chat_repository import (
    ChatResponseRepository,
)
import logging


"""
Data Service class is responsible for handling the data related operations.
When user requests for data, the data service interacts with the database repository.
"""
class DataService:

    def __call__(self) -> DataInterface:
        return self

    def __init__(
        self,
        database_repository=DatabaseRepository,
        chat_response_repository=ChatResponseRepository,
    ):
        self.database_repository = database_repository
        self.chat_response_repository = chat_response_repository

    def get_quantitative_metrics(self, user):
        try:
            # Get the general metrics for the user
            general_metrics = self.database_repository.find_single_document(
                "email", user, "quantitative_metrics"
            )
            general_metrics["data"] = general_metrics["data"]

            # Return the general metrics
            return general_metrics
        except Exception as e:
            logging.error(f"Failed to get general metrics: {e}")

    def get_assessment_metrics(self, user):
        try:
            # Get the assessment metrics for the user
            assessment_metrics = self.database_repository.find_single_document(
                "email", user, "assessment_metrics"
            )

            assessment_metrics["data"] = assessment_metrics["data"][::-1]

            # Return the assessment metrics
            return assessment_metrics
        except Exception as e:
            logging.error(f"Failed to get assessment metrics: {e}")
    
    """
    Schedule recommendations for all users. Not binded to any API endpoint. 
    Currently this function is called every day at 10:30 AM. However we may need
    to change this to a more dynamic approach.
    """
    def schedule_recommendations(self):
        try:
            # Get all the users
            all_users = self.database_repository.find_all_documents("users")

            with ThreadPoolExecutor() as executor:
                # Submit tasks for each user
                futures = [
                    executor.submit(self.process_user, user) for user in all_users
                ]

                # Wait for all tasks to complete
                for future in futures:
                    future.result()

        except Exception as e:
            logging.error(f"Failed to schedule recommendations: {e}")

    """
    Process the recommendations for a given user.
    Currenlty it retrieves the data three times from database for fetching different information. 
    1. quantitative_metrics
    2. assessment_metrics
    3. general_metrics

    Not a recommended approach as it increases the number of database calls. Need to refactor this code to reduce the number of database calls.
    """

    def process_user(self, user):
        try:
            user_email = user["email"]

            # Get the metrics for the user
            quantitative_metrics = self.database_repository.find_single_document(
                "email", user_email, "quantitative_metrics"
            )
            assessment_metrics = self.database_repository.find_single_document(
                "email", user_email, "assessment_metrics"
            )
            general_metrics = self.database_repository.find_single_document(
                "email", user_email, "general_metrics"
            )

            # Get the recommendations for the user through LLMs.
            recommendations = self.chat_response_repository.llm_recommendation(
                quantitative_metrics, assessment_metrics, general_metrics
            )

            if_data_exists = self.database_repository.find_single_document(
                "email", user_email, "recommendations"
            )

            if if_data_exists is not None:
                self.database_repository.update_single_document_(
                    "email",
                    user_email,
                    {"data": recommendations},
                    "recommendations",
                )
            else:
                self.database_repository.insert_single_document(
                    {"email": user_email, "data": [recommendations]},
                    "recommendations",
                )

            logging.info(f"Processed recommendations for user: {user_email}")

        except Exception as e:
            logging.error(
                f"Failed to process recommendations for user {user_email}: {e}"
            )

    def get_recommendations(self, user):
        try:
            # Get the recommendations for the user
            recommendations = self.database_repository.find_single_document(
                "email", user, "recommendations"
            )
            logging.info(recommendations)
            # Return the recommendations
            return recommendations["data"]
        except Exception as e:
            logging.error(f"Failed to get recommendations: {e}")
            return None

    def get_general_metrics(self, user):
        try:
            # Get the general metrics for the user
            general_metrics = self.database_repository.find_single_document(
                "email", user, "general_metrics"
            )
            # Return the general metrics
            return general_metrics
        except Exception as e:
            logging.error(f"Failed to get general metrics: {e}")
            return None

    def update_general_metrics(self, field, field_value, data, collection_name):
        try:
            update_metrics = self.database_repository.update_single_document(
                field, field_value, data, collection_name
            )

            return update_metrics

        except Exception as e:
            return None
