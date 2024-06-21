from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List


class ChatInterface(ABC):

    @abstractmethod
    def chat_response(
        self, user: str, query: str, all_messages: List[Dict[str, str]]
    ) -> None:
        """Generate a chat response based on the user, query, and previous messages."""
        pass

    @abstractmethod
    def llm_assessment(
        self, user: str, query: str, all_messages: List[Dict[str, str]]
    ) -> None:
        """Perform an LLM assessment based on the user, query, and previous messages."""
        pass

    @abstractmethod
    def llm_user_general_metrics(
        self, user: str, query: str, all_messages: List[Dict[str, str]]
    ) -> None:
        """Retrieve LLM user general metrics based on the user, query, and previous messages."""
        pass


    @abstractmethod
    async def streaming_llm_response(
        self, user: str, query: str, all_messages: List[Dict[str, str]]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Generate a streaming LLM response based on the user, query, and previous messages."""
        pass


    @abstractmethod
    async def streaming_voice_assessment_response(
        self, user: str, query: str, all_messages: List[Dict[str, str]]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Generate a streaming voice response based on the user, query, and previous messages."""
        pass


    @abstractmethod
    def get_fhir_data(self, encoded_image: str) -> None:
        """Get FHIR data from an encoded image."""
        pass

    @abstractmethod
    def general_chat_query(
        self, query: str, previous_messages: List[Dict[str, str]]
    ) -> None:
        """Perform a general chat query based on the query and previous messages."""
        pass

    @abstractmethod
    async def get_streaming_voice_response(
        self, query: str, previous_messages: List[Dict[str, str]]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Get a streaming voice response based on the query and previous messages."""
        pass
