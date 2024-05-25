from src.infastructure.repositories.chat_repository import ChatResponseRepository

class ChatService:

    def __call__(self) -> None:
        return self
    
    def __init__(self, chat_repository=ChatResponseRepository) -> None:
        self.chat_repository = chat_repository


    def chat_response(self, _query, all_messages):
        return self.chat_repository.chat_response(_query, all_messages)