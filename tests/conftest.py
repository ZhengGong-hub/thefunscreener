import os
import sys
import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now imports from both app and database modules should work
from app.database.db_task_manager import TaskManagerRepository
from app.database.postgres_database import PostgresDatabase
from app.config.config import Config

@pytest.fixture
def task_manager():
    """Create a TaskManagerRepository instance with test database."""
    config = Config().load_configuration()
    # Create database
    db = PostgresDatabase(**config.database.db_config)

    # Create task manager with schema
    manager = TaskManagerRepository(db)
    yield manager
