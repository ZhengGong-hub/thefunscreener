# there is no point to test the connection to the database by itself
# we will just test it here to make sure it's working
# considering the scale of the project, we will not be testing the database alone

def test_test_connection_query(task_manager):
    """Test querying global market cap."""
    result = task_manager.test_connection_query()
    assert result is not None
    assert len(result) == 10


def test_query_global_market_cap(task_manager):
    """Test querying global market cap.
    
    Three companies in Switzerland that have a market cap of more than 200B USD.
    """
    result = task_manager.query_global_market_cap(asofdate="2025-05-03", mktcap_thres=200e3, country="CH")
    assert result is not None
    assert len(result) == 3


def test_query_global_market_cap_all_countries(task_manager):
    """Test querying global market cap for all countries.
    
    Ten companies in the world that have a market cap of 1 trillion USD. (including one from Saudi)
    """
    result = task_manager.query_global_market_cap(asofdate="2025-05-12", mktcap_thres=1000e3, country="Global")
    assert result is not None
    assert len(result) == 10


def test_query_global_market_cap_top_x(task_manager):
    """Test querying global market cap for all countries.
    
    Ten companies in the world that have a market cap of 1 trillion USD. (including one from Saudi)
    """
    result = task_manager.query_global_market_cap(asofdate="2025-05-12", mktcap_thres=500e3, country="US", allow_fuzzy=True)
    assert result is not None
    assert len(result) > 20 # becasue of allow fuzzy try to capture for the last x days