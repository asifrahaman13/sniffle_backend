from abc import ABC, abstractmethod


class ChatInterface(ABC):
    @abstractmethod
    def chat_response(self, user, query, all_messages):
        pass

    @abstractmethod
    def llm_assessment(self, user, query, all_messages):
        pass

    @abstractmethod
    def llm_user_general_metrics(self, user, query, all_messages):
        pass

    @abstractmethod
    def streaming_llm_response(self, user, query, all_messages):
        pass

    @abstractmethod
    def streaming_voice_assessment_response(self, user, query, all_messages):
        pass

    @abstractmethod
    def get_fhir_data(self, encoded_image):
        pass
