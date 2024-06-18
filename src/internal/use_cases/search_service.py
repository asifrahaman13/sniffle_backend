
from typing import Dict, List

from src.infastructure.repositories.search_repository import SearchRepository
from src.internal.interfaces.search_interface import SearchInterface


class SearchService:

    def __call__(self) -> SearchInterface:
        return self
    
    def __init__(
        self, search_repository: SearchRepository = SearchRepository
    ) -> None:
        self.search_repository = search_repository

    def search(self, query_text: str) -> List[Dict]:
        print("Searching", query_text)
        search_results = self.search_repository.query_text(query_text)
        print(search_results)
        return search_results