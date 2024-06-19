from src.infastructure.repositories.chat_repository import (
    ChatResponseRepository,
)
from src.infastructure.repositories.database_repository import (
    DatabaseRepository,
)
import logging
import time


class ChatService:

    def __call__(self) -> None:
        return self

    def __init__(
        self,
        chat_repository=ChatResponseRepository,
        database_repository=DatabaseRepository,
    ) -> None:
        self.chat_repository = chat_repository
        self.database_repository = database_repository 

    def chat_response(self, user, query, all_messages):

        # Get the chat response
        response = self.chat_repository.chat_response(query, all_messages)

        # Check if the response is a summary
        if response["summary"] == True:
            try:

                # Check if the user exists in the database
                if_data_exists = self.database_repository.find_single_document(
                    "email", user, "quantitative_metrics"
                )

                # Add the timestamp to the response
                response["response_schema"]["timestamp"] = int(time.time())

                # Save the chat response
                if if_data_exists is not None:
                    self.database_repository.append_entity_to_array(
                        "email",
                        user,
                        "data",
                        response["response_schema"],
                        "quantitative_metrics",
                    )

                # If the user does not exist in the database, create a new document
                else:
                    self.database_repository.insert_single_document(
                        {"email": user, "data": [response["response_schema"]]},
                        "quantitative_metrics",
                    )

                # Return the response
                return response["response"]

            except Exception as e:
                logging.error(f"Failed to save chat response: {e}")
        else:
            return response["response"]

    def llm_assessment(self, user, query, all_messages):

        # Get the chat response
        response = self.chat_repository.llm_assessment(query, all_messages)

        # Check if the response is a summary
        if response["summary"] == True:
            try:

                # Check if the user exists in the database
                if_data_exists = self.database_repository.find_single_document(
                    "email", user, "assessment_metrics"
                )

                # Add the timestamp to the response
                response["response_schema"]["timestamp"] = int(time.time())

                # Save the chat response
                if if_data_exists is not None:
                    self.database_repository.append_entity_to_array(
                        "email",
                        user,
                        "data",
                        response["response_schema"],
                        "assessment_metrics",
                    )

                # If the user does not exist in the database, create a new document
                else:
                    self.database_repository.insert_single_document(
                        {"email": user, "data": [response["response_schema"]]},
                        "assessment_metrics",
                    )

                # Return the response
                return response["response"]

            except Exception as e:
                logging.error(f"Failed to save chat response: {e}")
        else:
            return response["response"]

    def llm_user_general_metrics(self, user, query, all_messages):

        try:

            # Get the general metrics for the user
            response = self.chat_repository.llm_user_general_metrics(query, all_messages)

            if response["summary"] == True:
                # Check if the user exists in the database
                if_data_exists = self.database_repository.find_single_document(
                    "email", user, "general_metrics"
                )

                if if_data_exists is None:

                    response["response_schema"]["email"] = user
                    # Add the timestamp to the response
                    response["response_schema"]["timestamp"] = int(time.time())

                    self.database_repository.insert_single_document(
                        response["response_schema"], "general_metrics"
                    )
                else:
                    # Add the timestamp to the response
                    response["response_schema"]["timestamp"] = int(time.time())
                    response["response_schema"]["email"] = user

                    # Save the chat response
                    self.database_repository.update_single_document(
                        "email",
                        user,
                        response["response_schema"],
                        "general_metrics",
                    )

                # Return the response
                return response["response"]

            # Check if the response is a summary
            return response["response"]
        except Exception as e:
            logging.error(f"Failed to get general metrics: {e}")

    def streaming_llm_response(self, user, query, all_messages):

        # Get the chat response
        responses = self.chat_repository.streaming_llm_response(query, all_messages)

        while True:

            response = next(responses)

            logging.info("Receiving the data", response)

            # Check if the response is a summary
            if response["is_last"] == True:
                logging.info(
                    "Updationg data to database the data",
                )
                try:

                    # Check if the user exists in the database
                    if_data_exists = self.database_repository.find_single_document(
                        "email", user, "quantitative_metrics"
                    )

                    logging.info(f"response: {if_data_exists}")

                    # Add the timestamp to the response
                    response["response_schema"]["timestamp"] = int(time.time())

                    # Save the chat response
                    if if_data_exists is not None:
                        self.database_repository.append_entity_to_array(
                            "email",
                            user,
                            "data",
                            response["response_schema"],
                            "quantitative_metrics",
                        )

                    # If the user does not exist in the database, create a new document
                    else:
                        self.database_repository.insert_single_document(
                            {
                                "email": user,
                                "data": [response["response_schema"]],
                            },
                            "quantitative_metrics",
                        )

                    # Return the response
                    return responses

                except Exception as e:
                    logging.error(f"Failed to save chat response: {e}")
            else:
                return responses

    def streaming_voice_assessment_response(self, user, query, all_messages):

        # Get the chat response
        responses = self.chat_repository.streaming_voice_assessment_response(query, all_messages)

        while True:

            response = next(responses)

            logging.info("Receiving the data", response)

            # Check if the response is a summary
            if response["is_last"] == True:
                logging.info(
                    "Updationg data to database the data",
                )
                try:

                    # Check if the user exists in the database
                    if_data_exists = self.database_repository.find_single_document(
                        "email", user, "assessment_metrics"
                    )

                    logging.info(f"response: {if_data_exists}")

                    # Add the timestamp to the response
                    response["response_schema"]["timestamp"] = int(time.time())

                    # Save the chat response
                    if if_data_exists is not None:
                        self.database_repository.append_entity_to_array(
                            "email",
                            user,
                            "data",
                            response["response_schema"],
                            "assessment_metrics",
                        )

                    # If the user does not exist in the database, create a new document
                    else:
                        self.database_repository.insert_single_document(
                            {
                                "email": user,
                                "data": [response["response_schema"]],
                            },
                            "assessment_metrics",
                        )

                    # Return the response
                    return responses

                except Exception as e:
                    logging.error(f"Failed to save chat response: {e}")
            else:
                return responses

    def get_fhir_data(self, encoded_image):
        return self.chat_repository.get_fhir_data(encoded_image)

    def general_chat_query(self, query, previous_messages):
        return self.chat_repository.general_chat_query(query, previous_messages)

    def get_streaming_voice_response(self, query, previous_messages):
        return self.chat_repository.get_streaming_voice_response(query, previous_messages)
