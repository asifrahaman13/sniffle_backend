from abc import ABC, abstractmethod

class AuthInterface(ABC):
    @abstractmethod
    def create_access_token(self, data):
        pass

    @abstractmethod
    def verify_google_access_token(self, token):
        pass

    @abstractmethod
    def decode_access_token(self, token):
        pass