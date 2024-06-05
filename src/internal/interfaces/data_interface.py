from abc import ABC, abstractmethod


class DataInterface(ABC):

    @abstractmethod
    def get_quantitative_metrics(self, user: str):
        pass

    @abstractmethod
    def get_assessment_metrics(self, user: str):
        pass

    @abstractmethod
    def schedule_recommendations(self):
        pass

    @abstractmethod
    def get_recommendations(self, user: str):
        pass

    @abstractmethod
    def get_general_metrics(self, user: str):
        pass

    @abstractmethod
    def update_general_metrics(self, field, field_value, data, collection_name):
        pass
