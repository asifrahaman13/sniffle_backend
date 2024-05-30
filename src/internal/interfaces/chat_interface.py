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
