import logging
from typing import Dict, List

from src.infastructure.repositories.search_repository import SearchRepository
from src.internal.interfaces.search_interface import SearchInterface


class SearchService:

    def __call__(self) -> SearchInterface:
        return self

    def __init__(self, search_repository: SearchRepository = SearchRepository) -> None:
        self.search_repository = search_repository

    def search(self, query_text: str) -> List[Dict]:
        logging.info("Searching")
        search_results = self.search_repository.query_text(query_text)
        logging.info(search_results)
        return search_results
