from src.infastructure.repositories.chat_repository import ChatResponseRepository

class ChatService:

    def __call__(self) -> None:
        return self
    
    def __init__(self, chat_repository=ChatResponseRepository) -> None:
        self.chat_repository = chat_repository


    def chat_response(self, _query):
        return self.chat_repository.chat_response(_query)