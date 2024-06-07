from src.infastructure.repositories.auth_repository import AuthRepository
from typing import Any, Dict


class AuthService:

    def __call__(self) -> "AuthService":
        return self

    def __init__(self, auth_repository: AuthRepository = AuthRepository) -> None:
        self.auth_repository = auth_repository

    def create_access_token(self, data: Dict[str, Any]) -> str:
        return self.auth_repository.create_access_token(data)

    def verify_google_access_token(self, token: str) -> Dict[str, Any]:
        return self.auth_repository.verify_google_access_token(token)

    def decode_access_token(self, token: str) -> Dict[str, Any]:
        return self.auth_repository.decode_access_token(token)
