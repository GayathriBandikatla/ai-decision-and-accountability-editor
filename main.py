"""Entry point for Patchamomma backend server."""

import logging
import os
import uvicorn
from config.settings import settings
from config.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def main():
    """Start the FastAPI server."""
    # Cloud Run injects PORT; local runs use API_PORT from .env
    port = int(os.environ.get("PORT", settings.api_port))
    logger.info("Starting Patchamomma server...")
    logger.info(f"Environment: DEBUG={settings.debug}")
    logger.info(f"API running on {settings.api_host}:{port}")

    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
    )


if __name__ == "__main__":
    main()
