from abc import ABC, abstractmethod


class SearchInterface(ABC):

    @abstractmethod
    def search(self, query: str) -> str:
        """Search for a given query."""
        pass
