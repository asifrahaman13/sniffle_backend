from abc import ABC, abstractmethod

class VoiceInterface(ABC):
    @abstractmethod
    def voice_response(self,query):
        pass