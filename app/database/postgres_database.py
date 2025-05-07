from typing import Optional, Any, Tuple, List
import psycopg2
import pandas as pd
from app.database.base_database import BaseDatabase
from app.utils.logging import get_logger
from contextlib import contextmanager
# Initialize logger
logger = get_logger(__name__)

class PostgresDatabase(BaseDatabase):
    """Postgres database class providing PostgresQL connection handling."""

    def __init__(self, dbname: str, user: str, password:str, host: str="localhost", port: int=5432):
        """Initialize database with configuration.

        Args:
            config: Database configuration containing connection details
        """
        self.config = dict(dbname=dbname, user=user, password=password, host=host, port=port)

        try:
            # Test connection
            conn = psycopg2.connect(**self.config)
            conn.close()
            logger.info(f"Successfully connected to database {dbname}@{host}")
        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(f"Failed to connect to database {dbname}@{host}: {e}")


    @contextmanager
    def get_connection(self):
        """Get database connection as context manager.

        Yields:
            Connection: Database connection
        """
        conn = psycopg2.connect(**self.config)
        try:
            yield conn
        finally:
            conn.close()

    def query_all(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """Execute a query and return all results.

        Args:
            query: SQL query to execute
            params: Query parameters

        Returns:
            list[tuple]: List of query results
        """
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            logger.info(f"{cur.query}: {cur.statusmessage}")
            result = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            df = pd.DataFrame(result, columns=column_names)
            return df
