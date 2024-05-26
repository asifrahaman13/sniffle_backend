from abc import ABC, abstractmethod

class DataInterface(ABC):

    @abstractmethod
    def get_general_metrics(self, user: str):
        pass