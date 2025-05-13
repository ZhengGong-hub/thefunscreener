# Api definition
# It uses a service and defines the endpoints to call the service methods
# No business logic, just binding a service to a REST endpoint
from fastapi import (
    APIRouter,
    Depends,
)
from app.api.api_service import TheFunScreenerService
from app.models.marketcap import MarketCapEntry
from app.api.auth import get_api_key


class TheFunScreenerAPI:
    def __init__(self, thefunscreener_service: TheFunScreenerService):
        self.router = APIRouter(tags=["thefunscreener"])
        self.thefunscreener_service = thefunscreener_service
        self._setup_routes()

    def _setup_routes(self):
        # Add root endpoint
        @self.router.get("/")
        async def read_root(api_key: str = Depends(get_api_key)):
            """Root endpoint."""
            return {"message": "Welcome to TheFunScreener API"}

        @self.router.get("/health")
        async def health_check(api_key: str = Depends(get_api_key)):
            """Health check endpoint for monitoring."""
            return {"status": "healthy"}

        @self.router.get("/latest-market-cap/{country}/{mktcap}/{top_x}")
        async def get_latest_market_cap(
            country: str,
            mktcap: str,
            top_x: int | None = None,
            api_key: str = Depends(get_api_key)
        ) -> list[MarketCapEntry]:
            return self.thefunscreener_service.get_latest_market_cap(country, mktcap, top_x)

        @self.router.get("/historical-market-cap/{country}/{mktcap}/{year}/{month}/{top_x}")
        async def get_historical_market_cap(
            country: str,
            mktcap: str,
            year: int,
            month: int,
            top_x: int | None = None,
            api_key: str = Depends(get_api_key)
        ) -> list[MarketCapEntry]:
            return self.thefunscreener_service.get_historical_market_cap(country, mktcap, year, month, top_x)
        
