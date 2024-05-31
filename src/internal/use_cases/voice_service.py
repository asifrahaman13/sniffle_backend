import logging
import time
from src.infastructure.repositories.voice_repository import VoiceRepository  
from src.infastructure.repositories.database_repository import DatabaseRepository
from src.infastructure.repositories.chat_repository import ChatResponseRepository
from src.internal.interfaces.voice_interface import VoiceInterface

class VoiceService:
    def __call__(self)->VoiceInterface:
        return self 
    
    def __init__(self,  database_repository=DatabaseRepository)->None:
        self.voice_repository = VoiceRepository()
        self.database_repository = DatabaseRepository()
        self.chat_repository = ChatResponseRepository()

    def voice_response(self, query):
        response = self.voice_repository.voice_response(query)
        return response