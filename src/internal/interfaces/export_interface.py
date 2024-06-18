from abc import ABC, abstractmethod
from typing import Any, Dict


class ExportInterface(ABC):
    @abstractmethod
    def export_data(self, user: str, collection_name:str) -> Any:
        """Send a notification to the user."""
        pass
