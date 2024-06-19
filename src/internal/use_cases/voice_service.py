from src.infastructure.repositories.voice_repository import VoiceRepository
from src.internal.interfaces.voice_interface import VoiceInterface


class VoiceService:
    def __call__(self) -> VoiceInterface:
        return self

    def __init__(self, voice_repository=VoiceRepository) -> None:
        self.voice_repository = voice_repository

    def voice_response(self, query: str) -> dict:
        response = self.voice_repository.voice_response(query)
        return response

    def voice_assessment_response(self, query: str) -> dict:
        response = self.voice_repository.voice_response(query)
        return response
