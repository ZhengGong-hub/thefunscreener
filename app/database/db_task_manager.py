from app.utils.logging import get_logger
from app.database.base_database import BaseDatabase
import pandas as pd
logger = get_logger(__name__)


class TaskManagerRepository:
    """Repository for handling task operations with api."""

    def __init__(self, database: BaseDatabase):
        """Initialize repository with database connection.

        Args:
            database: Database instance for data access
        """
        self.database = database

    def test_connection_query(self) -> pd.DataFrame:
        """Test the connection to the database.

        Returns:
            pd.DataFrame: A dataframe with the company ID.
        """
        return self.database.query_all("SELECT * from ciqcompany limit 10;")

    def query_global_market_cap(self, asofdate: str, mktcap_thres: float, country: str = "US", allow_fuzzy: bool = False) -> pd.DataFrame:
        """Query the global market cap that is above the threshold and at a given date.

        we do not really need the fuzzy, as the marketcap is pretty dense over vacations and holidays

        Args:
            asofdate: The date to query the market cap for
            mktcap_thres: The market cap threshold (in million USD)
            country: The country code to filter companies (default: "US")
            allow_fuzzy: If True, look for data within 5 days of asofdate if exact date not available

        Returns:
            pd.DataFrame: A dataframe with the company ID and market cap
        """
        # check asofdate is a str
        if not isinstance(asofdate, str):
            raise ValueError("asofdate must be a string")

        # Common SELECT fields and table joins for both scenarios
        query = """
            SELECT 
                ciqmarketcap.companyid,
                ciqmarketcap.marketcap,
                ciqmarketcap.pricingdate,
                round(ciqmarketcap.marketcap / ciqexchangerate.priceclose, 2) as usdmarketcap,
                ciqcompany.companyname,
                ciqtradingitem.tickersymbol,
                ciqcurrency.isocode as currency,
                ciqexchange.exchangesymbol as exchange
            FROM
                ciqmarketcap
            JOIN
                ciqcompany ON ciqmarketcap.companyID = ciqcompany.companyID
            JOIN
                ciqsecurity ON ciqmarketcap.companyID = ciqsecurity.companyID
            JOIN 
                ciqtradingitem on ciqsecurity.securityid = ciqtradingitem.securityid
            JOIN 
                ciqexchangerate on ciqtradingitem.currencyid = ciqexchangerate.currencyid
            JOIN
                ciqcurrency on ciqtradingitem.currencyid = ciqcurrency.currencyid
            JOIN
                ciqexchange on ciqtradingitem.exchangeid = ciqexchange.exchangeid
            JOIN 
                ciqcountrygeo on ciqcompany.countryid = ciqcountrygeo.countryid
            WHERE
        """

        # Date conditions differ based on allow_fuzzy
        if allow_fuzzy:
            query += f"""
                ciqmarketcap.pricingdate BETWEEN DATE('{asofdate}') - INTERVAL '5 days' AND '{asofdate}'
            """
        else:
            query += f"""
                ciqmarketcap.pricingdate = '{asofdate}'
            """

        # Common WHERE conditions for both scenarios
        query += f"""
            AND
                ciqexchangerate.pricedate = '{asofdate}'
            AND
                ciqexchangerate.latestsnapflag = 1
            AND
                ciqmarketcap.marketcap / ciqexchangerate.priceclose >= {mktcap_thres}
            AND 
                ciqcountrygeo.isocountry2 = '{country}'
            AND
                ciqcompany.companytypeid = 4
            AND 
                ciqsecurity.primaryflag = 1
            AND 
                ciqtradingitem.primaryflag = 1
            ORDER BY
                ciqmarketcap.pricingdate DESC, usdmarketcap DESC
        """

        res = self.database.query_all(query)
        # convert to dataframe
        df = pd.DataFrame(res)
        return df
