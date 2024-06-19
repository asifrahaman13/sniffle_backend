import logging
from typing import Dict, List
import openai
import qdrant_client
from qdrant_client.models import PointStruct, VectorParams, Distance
from config.config import OPEN_AI_API_KEY, EMBEDDING_MODEL
from src.constants.search.search import texts, metadata

"""
Embedding service is used to create embeddings from the text using OpenAI API.
Currently we are using the open ai embeddings but any open sourced embedding models can also be used.
"""


class EmbeddingService:
    """
    Embedding service to get embeddings from the text using OpenAI API.
    """

    def __init__(self):
        self.__openai_client = openai.Client(api_key=OPEN_AI_API_KEY)
        self.__embedding_model = EMBEDDING_MODEL
        self.__embeddings_cache: Dict[str, List[float]] = {}

    def get_embeddings(self, text: str) -> List[float]:
        """
        Check if the embeddings are already cached.
        If already cached then we do not need to perform the embeddings again.
        We can directly reuse the data from  cache. Currenlty its in memory cache.
        """
        if text in self.__embeddings_cache:
            return self.__embeddings_cache[text]
        else:
            result = self.__openai_client.embeddings.create(
                input=[text], model=self.__embedding_model
            )
            self.__embeddings_cache[text] = result.data[0].embedding
            return self.__embeddings_cache[text]


class QdrantService:

    """
    Qdrant client is used here to create collection, upsert points and search the points.
    """
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

    """
    Search repository is used to initialize the qdrant service and prepare the points.
    It also has the query_text method which is used to search the text.
    """
    def __init__(
        self, embedding_service: EmbeddingService, qdrant_service: QdrantService
    ):
        self.__embedding_service = embedding_service
        self.__qdrant_service = qdrant_service
    
    """
    Prepare the points from the text and metadata. Metadat includes the front end configuration 
    data for the screens.
    """
    def prepare_points(
        self, texts: List[str], metadata: List[Dict]
    ) -> List[PointStruct]:
        return [
            PointStruct(
                id=idx,
                vector=self.__embedding_service.get_embeddings(text),
                payload={"text": text, **meta},
            )
            for idx, (text, meta) in enumerate(zip(texts, metadata))
        ]
    """
    This function will be called before the start of the FastAPI application server.
    The function initialized the data points, creates collection and upserts the static data points.
    They will be later used as cached data for the vector search.
    """
    def initialize_qdrant(self):
        points = self.prepare_points(texts, metadata)
        self.__qdrant_service.create_collection()
        self.__qdrant_service.upsert_points(points)

    def query_text(self, query_text: str):
        try:
            # Get the embeddings for the query text.
            query_embedding = self.__embedding_service.get_embeddings(query_text)

            # Search the text using the embeddings.
            response = self.__qdrant_service.search(query_embedding)

            logging.info(f"Query: {query_text}")
            result = []
            for data in response:
                logging.info(f"Text: {data.payload['text']}")
                logging.info(f"Metadata: {data.payload}")
                result.append({"text": data.payload["text"], "metadata": data.payload})
            return result
        except Exception as e:
            logging.error(f"Failed to search: {e}")
            return []
