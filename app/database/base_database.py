from abc import ABC, abstractmethod
from typing import Tuple, List
from contextlib import contextmanager

class BaseDatabase(ABC):
    """Base database"""

    @contextmanager
    @abstractmethod
    def get_connection(self):
        """Get database connection as context manager.

        Yields:
            Connection: Database connection
        """
        pass

    @abstractmethod
    def query_all(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """Execute a query and return all results,
           use context manager 'with' clause.

        Args:
            query: SQL query to execute
            params: Query parameters

        Returns:
            list[tuple]: List of query results
        """
        pass

