import logging
from typing import Dict, List
import openai
import qdrant_client
from qdrant_client.models import PointStruct, VectorParams, Distance
from config.config import OPEN_AI_API_KEY, EMBEDDING_MODEL
from src.constants.search.search import texts, metadata


class EmbeddingService:
    def __init__(self, api_key: str, model: str):
        self.openai_client = openai.Client(api_key=api_key)
        self.embedding_model = model
        self.embeddings_cache: Dict[str, List[float]] = {}

    def get_embeddings(self, text: str) -> List[float]:
        if text in self.embeddings_cache:
            return self.embeddings_cache[text]
        else:
            result = self.openai_client.embeddings.create(input=[text], model=self.embedding_model)
            self.embeddings_cache[text] = result.data[0].embedding
            return self.embeddings_cache[text]


class QdrantService:
    def __init__(self):
        self.client = qdrant_client.QdrantClient(":memory:")
        self.collection_name = "example_collection"

    def create_collection(self):
        logging.info("Creating collection...")
        self.client.create_collection(
            self.collection_name,
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE,
            ),
        )
        logging.info("Collection created.")

    def upsert_points(self, points: List[PointStruct]):
        logging.info("Upserting points...")
        self.client.upsert(self.collection_name, points)
        logging.info("Points upserted.")

    def search(self, query_embedding: List[float], limit: int = 3):
        logging.info("Searching...")
        return self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
        )


class SearchRepository:
    def __init__(self, embedding_service: EmbeddingService, qdrant_service: QdrantService):
        self.embedding_service = embedding_service
        self.qdrant_service = qdrant_service

    def prepare_points(self, texts: List[str], metadata: List[Dict]) -> List[PointStruct]:
        return [
            PointStruct(
                id=idx,
                vector=self.embedding_service.get_embeddings(text),
                payload={"text": text, **meta},
            )
            for idx, (text, meta) in enumerate(zip(texts, metadata))
        ]

    def initialize_qdrant(self):
        points = self.prepare_points(texts, metadata)
        self.qdrant_service.create_collection()
        self.qdrant_service.upsert_points(points)

    def query_text(self, query_text: str):
        try:
            query_embedding = self.embedding_service.get_embeddings(query_text)
            response = self.qdrant_service.search(query_embedding)

            logging.info(f"Query: {query_text}")
            result = []
            for data in response:
                logging.info(f"Text: {data.payload['text']}")
                logging.info(f"Metadata: {data.payload}")
                result.append({"text": data.payload["text"], "metadata": data.payload})
            logging.info("*******************************\n\n\n\n")
            return result
        except Exception as e:
            logging.error(f"Failed to search: {e}")
            return []


# Initialize services
api_key = OPEN_AI_API_KEY
embedding_model = EMBEDDING_MODEL

embedding_service = EmbeddingService(api_key, embedding_model)
qdrant_service = QdrantService()
search_repository = SearchRepository(embedding_service, qdrant_service)
