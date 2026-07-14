from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # =====================================================
    # LLM Provider
    # =====================================================

    LLM_PROVIDER: str = "groq"

    LLM_MODEL: str = "llama-3.3-70b-versatile"

    GROQ_API_KEY: str = ""

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    OPENAI_API_KEY: str = ""

    GEMINI_API_KEY: str = ""

    # =====================================================
    # Embedding
    # =====================================================

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    CROSS_ENCODER_MODEL: str = (
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    EMBEDDING_DIM: int = 384

    # =====================================================
    # Qdrant
    # =====================================================

    QDRANT_HOST: str = "127.0.0.1"

    QDRANT_PORT: int = 6333

    COLLECTION_NAME: str = "rag_documents"

    # =====================================================
    # Redis
    # =====================================================

    REDIS_HOST: str = "127.0.0.1"

    REDIS_PORT: int = 6379

    REDIS_DB: int = 0

    CACHE_TTL: int = 3600
    # =====================================================
    # Chunking
    # =====================================================

    PARENT_CHUNK_SIZE: int = 3000

    PARENT_OVERLAP: int = 300

    CHILD_CHUNK_SIZE: int = 800

    CHILD_OVERLAP: int = 150

    # =====================================================
    # Paths
    # =====================================================

    RAW_DATA_PATH: str = "data/raw"

    REGISTRY_FILE: str = "document_registry.json"

    ACTIVE_DOCUMENT_FILE: str = "active_document.json"

    # =====================================================
    # ENV
    # =====================================================

    class Config:

        env_file = ".env"

        extra = "ignore"


settings = Settings()