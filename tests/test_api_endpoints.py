import pytest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a FastAPI test client."""
    return TestClient(app)


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "API is running"}


@patch('app.db.database.DatabaseManager.execute_query')
def test_db_health_check(mock_execute_query, client):
    """Test the database health check endpoint."""
    # Mock successful DB connection
    mock_execute_query.return_value = [{"1": 1}]

    response = client.get("/api/v1/health/db")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Database connection successful"}

    # Mock DB connection failure
    mock_execute_query.side_effect = Exception("Connection failed")

    response = client.get("/api/v1/health/db")
    assert response.status_code == 200
    assert response.json()["status"] == "error"
    assert "Connection failed" in response.json()["message"]


@patch('app.services.company_service.CompanyService.get_top_market_cap_companies')
def test_get_top_companies(mock_get_top, client):
    """Test getting top companies endpoint."""
    # Mock data
    mock_data = [
        {
            "id": 1,
            "ticker": "AAPL",
            "name": "Apple Inc.",
            "market_cap": 2500000000000,
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "country": "United States",
            "last_updated": "2023-06-01T00:00:00"
        },
        {
            "id": 2,
            "ticker": "MSFT",
            "name": "Microsoft Corporation",
            "market_cap": 2300000000000,
            "sector": "Technology",
            "industry": "Software",
            "country": "United States",
            "last_updated": "2023-06-01T00:00:00"
        }
    ]
    mock_get_top.return_value = mock_data

    # Test default limit
    response = client.get("/api/v1/companies/top")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["ticker"] == "AAPL"
    assert mock_get_top.call_args[1]["limit"] == 100

    # Test custom limit
    response = client.get("/api/v1/companies/top?limit=10")
    assert response.status_code == 200
    assert mock_get_top.call_args[1]["limit"] == 10


@patch('app.services.company_service.CompanyService.get_company_by_ticker')
def test_get_company(mock_get_company, client):
    """Test getting a company by ticker endpoint."""
    # Mock data
    mock_data = {
        "id": 1,
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "market_cap": 2500000000000,
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "country": "United States",
        "last_updated": "2023-06-01T00:00:00"
    }
    mock_get_company.return_value = mock_data

    # Test getting existing company
    response = client.get("/api/v1/companies/AAPL")
    assert response.status_code == 200
    assert response.json()["ticker"] == "AAPL"
    assert response.json()["name"] == "Apple Inc."

    # Test getting non-existent company
    mock_get_company.return_value = None
    response = client.get("/api/v1/companies/NONEXISTENT")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


@patch('app.services.company_service.CompanyService.create_company')
@patch('app.services.company_service.CompanyService.get_company_by_ticker')
def test_create_company(mock_get_company, mock_create_company, client):
    """Test creating a company endpoint."""
    # Mock data
    company_data = {
        "ticker": "META",
        "name": "Meta Platforms Inc.",
        "market_cap": 900000000000,
        "sector": "Technology",
        "industry": "Internet Content & Information",
        "country": "United States"
    }

    created_company = {
        "id": 5,
        "ticker": "META",
        "name": "Meta Platforms Inc.",
        "market_cap": 900000000000,
        "sector": "Technology",
        "industry": "Internet Content & Information",
        "country": "United States",
        "last_updated": "2023-06-01T00:00:00"
    }

    # Mock non-existent company for first call
    mock_get_company.return_value = None
    mock_create_company.return_value = created_company

    # Test creating a new company
    response = client.post("/api/v1/companies/", json=company_data)
    assert response.status_code == 200
    assert response.json()["ticker"] == "META"
    assert response.json()["id"] == 5

    # Mock existing company for second call
    mock_get_company.return_value = created_company

    # Test creating an existing company
    response = client.post("/api/v1/companies/", json=company_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


@patch('app.tasks.market_data_updater.MarketDataUpdater.update_market_data')
def test_update_market_data(mock_update_market_data, client):
    """Test updating market data endpoint."""
    # Mock successful update
    mock_update_market_data.return_value = 5

    response = client.post("/api/v1/companies/update-market-data")
    assert response.status_code == 200
    assert response.json()["detail"] == "Updated 5 companies with latest market data"
