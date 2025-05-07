import pytest
from unittest.mock import patch, MagicMock

from app.tasks.market_data_updater import MarketDataUpdater
from app.models.company import CompanyCreate


@pytest.fixture
def mock_company_data():
    """Mock company data for testing."""
    return [
        {
            "ticker": "AAPL",
            "name": "Apple Inc.",
            "market_cap": 2500000000000,
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "country": "United States"
        },
        {
            "ticker": "MSFT",
            "name": "Microsoft Corporation",
            "market_cap": 2300000000000,
            "sector": "Technology",
            "industry": "Software",
            "country": "United States"
        },
        {
            "ticker": "GOOGL",
            "name": "Alphabet Inc.",
            "market_cap": 1800000000000,
            "sector": "Technology",
            "industry": "Internet Content & Information",
            "country": "United States"
        }
    ]


def test_fetch_top_market_cap_companies():
    """Test fetching top market cap companies."""
    # The MarketDataUpdater._get_mock_data() method already provides test data
    # so we can just call the fetch method directly
    companies = MarketDataUpdater.fetch_top_market_cap_companies()
    
    # Verify we have data
    assert len(companies) > 0
    assert "ticker" in companies[0]
    assert "name" in companies[0]
    assert "market_cap" in companies[0]


@patch('app.services.company_service.CompanyService.upsert_company')
@patch('app.tasks.market_data_updater.MarketDataUpdater.fetch_top_market_cap_companies')
def test_update_market_data(mock_fetch, mock_upsert, mock_company_data):
    """Test updating market data."""
    # Mock the fetch method to return our test data
    mock_fetch.return_value = mock_company_data
    
    # Mock the upsert method to return the input data
    mock_upsert.side_effect = lambda x: x.dict()
    
    # Call the update method
    count = MarketDataUpdater.update_market_data()
    
    # Verify the results
    assert count == 3
    assert mock_fetch.call_count == 1
    assert mock_upsert.call_count == 3
    
    # Verify the correct company objects were created
    calls = mock_upsert.call_args_list
    assert isinstance(calls[0][0][0], CompanyCreate)
    assert calls[0][0][0].ticker == "AAPL"
    assert calls[1][0][0].ticker == "MSFT"
    assert calls[2][0][0].ticker == "GOOGL"


@patch('app.tasks.market_data_updater.MarketDataUpdater.update_market_data')
def test_run_daily_update(mock_update):
    """Test running the daily update task."""
    # Mock the update method
    mock_update.return_value = 3
    
    # Import here to avoid circular imports
    from app.tasks.market_data_updater import run_daily_update
    
    # Run the daily update
    run_daily_update()
    
    # Verify the update method was called
    assert mock_update.call_count == 1 