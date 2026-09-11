"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration from .env file."""

    # Gemini API
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.6-flash"
    # Comma-separated, tried in order when the primary fails (e.g. per-model free-tier quota)
    gemini_fallback_models: str = (
        "gemini-3.5-flash,gemini-3.8-flash,gemini-3.5-flash-lite,"
        "gemini-3.1-flash-lite,gemini-flash-lite-latest"
    )

    # Google Cloud
    gcp_project_id: str = ""
    gcp_credentials_path: Optional[str] = None

    # BigQuery
    bq_dataset_id: str = "patchamomma"
    bq_table_decisions: str = "decisions"
    bq_table_actions: str = "action_items"

    # Firestore
    firestore_collection: str = "decision_ledger"

    # FastAPI
    api_port: int = 8080
    api_host: str = "0.0.0.0"
    debug: bool = False

    # React Frontend
    react_app_api_url: str = "http://localhost:8000"

    class Config:
        """Load from .env file."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create settings instance
settings = Settings()
