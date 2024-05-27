from src.infastructure.repositories.chat_repository import ChatResponseRepository
from src.infastructure.repositories.database_repository import DatabaseRepository
import logging
import time

class ChatService:

    def __call__(self) -> None:
        return self
    
    def __init__(self, chat_repository=ChatResponseRepository, database_repository=DatabaseRepository ) -> None:
        self.chat_repository = chat_repository
        self.database_repository = DatabaseRepository()


    def chat_response(self, user, query, all_messages):

        # Get the chat response
        response=self.chat_repository.chat_response(query, all_messages)

        # Check if the response is a summary
        if response["summary"]==True:
            try:
                
                # Check if the user exists in the database
                if_data_exists=self.database_repository.find_single_document("email", user, "general_metrics")

                # Add the timestamp to the response
                response["response_schema"]["timestamp"]=int(time.time())

                # Save the chat response
                if if_data_exists is not None:
                    self.database_repository.append_entity_to_array("email", user, "data", response["response_schema"], "general_metrics")

                # If the user does not exist in the database, create a new document
                else:
                    self.database_repository.insert_single_document({"email": user, "data": [response["response_schema"]]}, "general_metrics")

                # Return the response
                return response["response"]

            except Exception as e:
                logging.error(f"Failed to save chat response: {e}")
        else: 
            return response["response"]

    def llm_assessment(self, user, query, all_messages):
            
            # Get the chat response
            response=self.chat_repository.llm_assessment(query, all_messages)
    
            # Check if the response is a summary
            if response["summary"]==True:
                try:
                    
                    # Check if the user exists in the database
                    if_data_exists=self.database_repository.find_single_document("email", user, "assessment_metrics")
    
                    # Add the timestamp to the response
                    response["response_schema"]["timestamp"]=int(time.time())
    
                    # Save the chat response
                    if if_data_exists is not None:
                        self.database_repository.append_entity_to_array("email", user, "data", response["response_schema"], "assessment_metrics")
    
                    # If the user does not exist in the database, create a new document
                    else:
                        self.database_repository.insert_single_document({"email": user, "data": [response["response_schema"]]}, "assessment_metrics")
    
                    # Return the response
                    return response["response"]
    
                except Exception as e:
                    logging.error(f"Failed to save chat response: {e}")
            else: 
                return response["response"] 