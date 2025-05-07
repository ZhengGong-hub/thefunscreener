# TheFunScreener

A FastAPI backend for screening stock companies by market capitalization.

## Features

- Database integration with PostgreSQL using psycopg2
- Daily updates of top 100 market cap companies
- RESTful API endpoints for querying company data
- Extensible architecture for future enhancements

## Prerequisites

- Python 3.9+
- PostgreSQL
- uv (for package management)

## Quick Setup

### On Unix/Linux/macOS

```bash
# Run the setup script
./scripts/setup_dev.sh
```

### On Windows (PowerShell)

```powershell
# Run the setup script
.\scripts\setup_dev.ps1
```

## Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/thefunscreener.git
   cd thefunscreener
   ```

2. Create a virtual environment with uv:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. Install dependencies using uv:
   ```bash
   # For production
   uv pip install .
   
   # For development (includes testing tools)
   uv pip install -e ".[dev]"
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file with your actual configuration.

## Database Setup

1. Create a PostgreSQL database:
   ```bash
   createdb thefunscreener
   ```

2. Initialize the database:
   ```bash
   python -m app.db.init_db
   ```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000.

Swagger/OpenAPI documentation is available at http://localhost:8000/api/v1/docs.

## Testing

### Running Unit Tests

Run all tests with pytest:

```bash
pytest
```

Run specific test files:

```bash
pytest tests/test_company_service.py
```

### Standalone Test Scripts

These scripts can be used to test specific components without starting the full API:

#### Database Connection Test

Tests database connectivity and basic operations:

```bash
python scripts/test_db_connection.py
```

#### Market Data Test

Tests fetching and updating market data:

```bash
python scripts/test_market_data.py
```

## Docker Deployment


### Linting with Ruff

```bash
ruff check .
```

## Connect to ciqDB
psql -h 101.46.32.216 -U qian -d targetdb -p 5432
"3nhf2f84228cf2f"

## API Endpoints

- `GET /api/v1/companies` - List all companies
- `GET /api/v1/companies/top` - Get top market cap companies
- `GET /api/v1/companies/{ticker}` - Get company by ticker
- `GET /api/v1/companies/search?q={query}` - Search companies
- `POST /api/v1/companies` - Create a new company
- `PUT /api/v1/companies/{ticker}` - Update a company
- `DELETE /api/v1/companies/{ticker}` - Delete a company
- `POST /api/v1/companies/update-market-data` - Manually update market data

## License

MIT