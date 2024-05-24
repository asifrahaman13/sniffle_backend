from abc import ABC, abstractmethod

class ChatInterface(ABC):
    @abstractmethod
    def chat_response(self, _query):
        pass