# there is no point to test the connection to the database by itself 
# we will just test it here to make sure it's working
# considering the scale of the project, we will not be testing the database alone
import pytest

def test_test_connection_query(task_manager):
    """Test querying global market cap."""
    result = task_manager.test_connection_query()
    assert result is not None
    assert len(result) == 10
