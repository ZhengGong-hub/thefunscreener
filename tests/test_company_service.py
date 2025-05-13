
from app.models.company import CompanyCreate, CompanyUpdate
from app.services.company_service import CompanyService


def test_create_company(mock_db_manager, test_db_connection):
    """Test creating a company."""
    # Create test company data
    company_data = CompanyCreate(
        ticker="TEST",
        name="Test Company",
        market_cap=1000000000,
        sector="Technology",
        industry="Software",
        country="United States"
    )

    # Create company
    result = CompanyService.create_company(company_data)

    # Check result
    assert result is not None
    assert result["ticker"] == "TEST"
    assert result["name"] == "Test Company"
    assert float(result["market_cap"]) == 1000000000
    assert result["sector"] == "Technology"

    # Verify in database
    with test_db_connection.cursor() as cursor:
        cursor.execute("SELECT * FROM companies WHERE ticker = 'TEST'")
        db_result = cursor.fetchone()
        assert db_result is not None
        assert db_result[1] == "TEST"  # ticker
        assert db_result[2] == "Test Company"  # name


def test_get_company_by_ticker(mock_db_manager, test_db_connection):
    """Test getting a company by ticker."""
    # Insert test data
    with test_db_connection.cursor() as cursor:
        cursor.execute("""
        INSERT INTO companies (ticker, name, market_cap, sector, industry, country)
        VALUES ('AAPL', 'Apple Inc.', 2500000000000, 'Technology', 'Consumer Electronics', 'United States')
        """)

    # Get company
    result = CompanyService.get_company_by_ticker("AAPL")

    # Check result
    assert result is not None
    assert result["ticker"] == "AAPL"
    assert result["name"] == "Apple Inc."
    assert float(result["market_cap"]) == 2500000000000

    # Test non-existent company
    result = CompanyService.get_company_by_ticker("NONEXISTENT")
    assert result is None


def test_update_company(mock_db_manager, test_db_connection):
    """Test updating a company."""
    # Insert test data
    with test_db_connection.cursor() as cursor:
        cursor.execute("""
        INSERT INTO companies (ticker, name, market_cap, sector, industry, country)
        VALUES ('MSFT', 'Microsoft Corporation', 2300000000000, 'Technology', 'Software', 'United States')
        """)

    # Update company
    update_data = CompanyUpdate(
        name="Microsoft Corp",
        market_cap=2400000000000
    )
    result = CompanyService.update_company("MSFT", update_data)

    # Check result
    assert result is not None
    assert result["ticker"] == "MSFT"
    assert result["name"] == "Microsoft Corp"
    assert float(result["market_cap"]) == 2400000000000

    # Verify in database
    with test_db_connection.cursor() as cursor:
        cursor.execute("SELECT * FROM companies WHERE ticker = 'MSFT'")
        db_result = cursor.fetchone()
        assert db_result is not None
        assert db_result[2] == "Microsoft Corp"  # name


def test_delete_company(mock_db_manager, test_db_connection):
    """Test deleting a company."""
    # Insert test data
    with test_db_connection.cursor() as cursor:
        cursor.execute("""
        INSERT INTO companies (ticker, name, market_cap, sector, industry, country)
        VALUES ('GOOGL', 'Alphabet Inc.', 1800000000000, 'Technology', 'Internet Content & Information', 'United States')
        """)

    # Delete company
    result = CompanyService.delete_company("GOOGL")
    assert result is True

    # Verify in database
    with test_db_connection.cursor() as cursor:
        cursor.execute("SELECT * FROM companies WHERE ticker = 'GOOGL'")
        db_result = cursor.fetchone()
        assert db_result is None


def test_get_top_market_cap_companies(mock_db_manager, test_db_connection):
    """Test getting top market cap companies."""
    # Insert test data
    test_companies = [
        ('AAPL', 'Apple Inc.', 2500000000000),
        ('MSFT', 'Microsoft Corporation', 2300000000000),
        ('GOOGL', 'Alphabet Inc.', 1800000000000),
        ('AMZN', 'Amazon.com Inc.', 1700000000000),
        ('NVDA', 'NVIDIA Corporation', 1200000000000)
    ]

    with test_db_connection.cursor() as cursor:
        for ticker, name, market_cap in test_companies:
            cursor.execute("""
            INSERT INTO companies (ticker, name, market_cap, sector)
            VALUES (%s, %s, %s, 'Technology')
            """, (ticker, name, market_cap))

    # Get top 3 companies
    result = CompanyService.get_top_market_cap_companies(limit=3)

    # Check result
    assert len(result) == 3
    assert result[0]["ticker"] == "AAPL"
    assert result[1]["ticker"] == "MSFT"
    assert result[2]["ticker"] == "GOOGL"


def test_search_companies(mock_db_manager, test_db_connection):
    """Test searching companies."""
    # Insert test data
    test_companies = [
        ('AAPL', 'Apple Inc.', 2500000000000),
        ('MSFT', 'Microsoft Corporation', 2300000000000),
        ('GOOGL', 'Alphabet Inc.', 1800000000000),
        ('AMZN', 'Amazon.com Inc.', 1700000000000),
        ('NVDA', 'NVIDIA Corporation', 1200000000000)
    ]

    with test_db_connection.cursor() as cursor:
        for ticker, name, market_cap in test_companies:
            cursor.execute("""
            INSERT INTO companies (ticker, name, market_cap, sector)
            VALUES (%s, %s, %s, 'Technology')
            """, (ticker, name, market_cap))

    # Search for "corp"
    result = CompanyService.search_companies("corp")

    # Check result
    assert len(result) == 2
    assert "Microsoft Corporation" in [r["name"] for r in result]
    assert "NVIDIA Corporation" in [r["name"] for r in result]

    # Search for "AA"
    result = CompanyService.search_companies("AA")
    assert len(result) == 1
    assert result[0]["ticker"] == "AAPL"
