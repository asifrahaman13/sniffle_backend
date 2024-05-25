import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve environment variables and ensure they are set
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
assert GOOGLE_CLIENT_ID, "Google client ID is not set"
logging.info("Google client ID is set")

SECRET_KEY = os.getenv("SECRET_KEY")
assert SECRET_KEY, "Secret key is not set"
logging.info("Secret key is set")

ALGORITHM = os.getenv("ALGORITHM")
assert ALGORITHM, "Algorithm is not set"
logging.info("Algorithm is set")

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
assert ACCESS_TOKEN_EXPIRE_MINUTES, "Access token expire minutes is not set"
logging.info("Access token expire minutes is set")


OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPEN_AI_API_KEY, "OpenAI client is not set"
logging.info("OpenAI client is set")