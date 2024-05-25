from src.infastructure.repositories.auth_repository import AuthRepository

class AuthService:

    def __call__(self) -> None:
        return self
    
    def __init__(self, auth_repository=AuthRepository) -> None:
        self.auth_repository=auth_repository

    def create_access_token(self, data):
        return self.auth_repository.create_access_token(data)
    
    def verify_google_access_token(self, token):
        return self.auth_repository.verify_google_access_token(token)
    
    def decode_access_token(self, token):
        return self.auth_repository.decode_access_token(token)