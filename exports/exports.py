from src.ConnectionManager.ConnectionManager import ConnectionManager
from src.infastructure.repositories.aws_repository import AWSRepository
from src.internal.use_cases.aws_service import AwsService
from src.internal.use_cases.data_service import DataService
from src.internal.use_cases.search_service import SearchService
from src.infastructure.repositories.export_repository import ExportRepository
from src.internal.use_cases.export_service import ExportService
from src.infastructure.repositories.voice_repository import VoiceRepository
from src.internal.use_cases.voice_service import VoiceService
from src.internal.use_cases.chat_service import ChatService
from src.infastructure.repositories.chat_repository import ChatResponseRepository
from src.infastructure.repositories.database_repository import (
    DatabaseRepository,
)
from src.infastructure.repositories.auth_repository import AuthRepository
from src.internal.use_cases.auth_service import AuthService
from src.internal.use_cases.database_service import DatabaseService
from src.infastructure.repositories.search_repository import EmbeddingService, QdrantService, SearchRepository

# Create a connection manager
manager = ConnectionManager()

database_repository = DatabaseRepository()
database_service = DatabaseService(database_repository)
auth_repository = AuthRepository()
auth_service = AuthService(auth_repository)

chat_response_repository = ChatResponseRepository()
chat_service = ChatService(chat_response_repository, database_repository)

auth_repository = AuthRepository()
auth_service = AuthService(auth_repository)

voice_repository = VoiceRepository()
voice_service = VoiceService(voice_repository)

export_repository = ExportRepository()
database_repository = DatabaseRepository()
export_service = ExportService(database_repository, export_repository)

data_service = DataService(database_repository, chat_response_repository)

aws_repository = AWSRepository()
aws_service = AwsService(aws_repository)

embedding_service = EmbeddingService()
qdrant_service = QdrantService()
search_repository = SearchRepository(embedding_service, qdrant_service)
search_service = SearchService(search_repository)