from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import APIRouter
from app.utils.logging import get_logger

# Initialize logger
logger = get_logger(__name__)


class TheFunScreenerServer:
    """Server class handling FastAPI setup and authentication."""

    def __init__(self):
        """Initialize server with configuration."""
        self.app = self.setup_web_app()

    def setup_web_app(self) -> FastAPI:
        """Set up and configure the FastAPI application.

        Returns:
            FastAPI: Configured FastAPI application
        """
        app = FastAPI(
            title="TheFunScreener API",
            # TODO: make the api version dynamic
            # TODO: this should only be available in dev
            openapi_url="/api/v1/openapi.json",
            description="API for thefunscreener",
            version="1.0.0",
        )

        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            # In production, replace with specific origins
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        return app

    def add_routes(self, router: APIRouter) -> None:
        """Add routes to the FastAPI application.

        Args:
            router: The APIRouter to add routes from.
        """
        self.app.include_router(router)

    def run(self) -> None:
        """Run the FastAPI application."""
        uvicorn.run(self.app, host="0.0.0.0", port=8033, reload=False)
