from abc import ABC, abstractmethod
from typing import Dict, Any


class VoiceInterface(ABC):

    @abstractmethod
    def voice_response(self, query: str) -> Dict[str, Any]:
        """Generate a voice response for the given query."""
        pass

    @abstractmethod
    def voice_assessment_response(self, query: str) -> Dict[str, Any]:
        """Generate a voice assessment response for the given query."""
        pass
