from src.internal.interfaces.data_interface import DataInterface
from src.infastructure.repositories.database_repository import DatabaseRepository
from src.infastructure.repositories.chat_repository import ChatResponseRepository
import logging

class DataService:

    def __call__(self) -> DataInterface:
        return self
    
    def __init__(self):
        self.database_repository = DatabaseRepository()
        self.chat_response_repository = ChatResponseRepository()

    def get_general_metrics(self, user):
        try:
            # Get the general metrics for the user
            general_metrics = self.database_repository.find_single_document("email", user, "general_metrics")
            # Return the general metrics
            return general_metrics
        except Exception as e:
            logging.error(f"Failed to get general metrics: {e}")

    def get_assessment_metrics(self, user):
        try:
            # Get the assessment metrics for the user
            assessment_metrics = self.database_repository.find_single_document("email", user, "assessment_metrics")
            # Return the assessment metrics
            return assessment_metrics
        except Exception as e:
            logging.error(f"Failed to get assessment metrics: {e}")

    def schedule_recommendations(self):
        try:

            # Get all the users
            all_users=self.database_repository.find_all_documents("users")
            for users in all_users:
                user=users["email"]
                # return {"message":"Recommendations are not available at the moment"}
                # Get the general and assessment metrics for the user
                general_metrics = self.database_repository.find_single_document("email", user, "general_metrics")

                logging.info(f"general_metrics: {general_metrics}")
                
                assessment_metrics = self.database_repository.find_single_document("email", user, "assessment_metrics")

                logging.info(f"assessment_metrics: {assessment_metrics}")
    
                # Get the recommendations for the user
                recommendations = self.chat_response_repository.llm_recommendation(general_metrics, assessment_metrics)

                logging.info(f"recommendations received: {recommendations}")
                
                # check if the user exists in the database
                if_data_exists=self.database_repository.find_single_document("email", user, "recommendations")

                # if if_data_exists is not None:
                #     # Append the recommendations to the existing document
                #     self.database_repository.append_entity_to_array("email", user, "data", recommendations["recommendations"], "recommendations", )
                # else:
                self.database_repository.insert_single_document({"email": user, "data": [recommendations]}, "recommendations")

            # Return the recommendations
            # return recommendations
        except Exception as e:
            logging.error(f"Sorry we  to get recommendations: {e}")


    def get_recommendations(self, user):
        try:
            # Get the recommendations for the user
            recommendations = self.database_repository.find_single_document("email", user, "recommendations")
            # Return the recommendations
            return recommendations["data"][0]
        except Exception as e:
            logging.error(f"Failed to get recommendations: {e}")
            return None