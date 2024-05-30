from datetime import datetime, timedelta
from datetime import UTC
from jose import jwt
from google.oauth2 import id_token
from google.auth.transport import requests
from config.config import GOOGLE_CLIENT_ID, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


class AuthRepository:

    def __init__(self) -> None:
        self.secret_key = SECRET_KEY
        self.google_client_id = GOOGLE_CLIENT_ID
        self.algorithm = ALGORITHM
        self.expires = 3600

    def create_access_token(self, data: dict):
        # Create a new access token
        to_encode = data.copy()

        # Set the expiration time for the token
        expire = datetime.now(UTC) + timedelta(minutes=self.expires)

        # Add the expiration time to the token
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_google_access_token(self, token):
        try:
            # Verify the access token
            id_info = id_token.verify_oauth2_token(token, requests.Request(), self.google_client_id)

            # Return the user information
            return id_info
        except ValueError:
            # Invalid token
            return None

    def decode_access_token(self, token):
        try:
            # Decode the access token
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            # Return the payload
            return payload
        except jwt.ExpiredSignatureError:
            # Token has expired
            return {"error": "Token has expired"}
        except jwt.JWTError:
            # Invalid token
            return {"error": "Invalid token"}
