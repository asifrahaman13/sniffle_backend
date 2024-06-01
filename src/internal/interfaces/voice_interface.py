from abc import ABC, abstractmethod

class VoiceInterface(ABC):
    @abstractmethod
    def voice_response(self,query):
        pass

    @abstractmethod
    def voice_assessment_response(self, query):
        pass