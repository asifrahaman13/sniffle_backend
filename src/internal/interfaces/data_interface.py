from abc import ABC, abstractmethod
from typing import Any, Dict


class DataInterface(ABC):

    @abstractmethod
    def get_quantitative_metrics(self, user: str) -> Dict[str, Any]:
        """Retrieve quantitative metrics for a given user."""
        pass

    @abstractmethod
    def get_assessment_metrics(self, user: str) -> Dict[str, Any]:
        """Retrieve assessment metrics for a given user."""
        pass

    @abstractmethod
    def schedule_recommendations(self) -> None:
        """Schedule recommendations for users."""
        pass

    @abstractmethod
    def get_recommendations(self, user: str) -> Dict[str, Any]:
        """Retrieve recommendations for a given user."""
        pass

    @abstractmethod
    def get_general_metrics(self, user: str) -> Dict[str, Any]:
        """Retrieve general metrics for a given user."""
        pass

    @abstractmethod
    def update_general_metrics(
        self, field: str, field_value: Any, data: Dict[str, Any], collection_name: str
    ) -> None:
        """Update general metrics in the specified collection."""
        pass
