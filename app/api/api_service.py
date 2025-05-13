from datetime import datetime
from app.database.db_task_manager import TaskManagerRepository
from app.utils.logging import get_logger
from app.utils.helper import convert_mktcap_to_number
from app.models.marketcap import MarketCapEntry


logger = get_logger(__name__)

class TheFunScreenerService:
    def __init__(self, task_manager: TaskManagerRepository):
        self.task_manager = task_manager


    def get_latest_market_cap(self, country: str, mktcap: str, top_x: int | None = None) -> list[MarketCapEntry]:
        """
        Get the latest market cap for a given country and market cap category

        Args:
            country: The country to get the market cap for
            mktcap: The market cap category, can take values "mega", "large", "mid"

        Returns:
            list[MarketCapEntry]: A list of market cap entries
        """
        mktcap_thres = convert_mktcap_to_number(mktcap)

        # get the latest trading date
        today = datetime.now().strftime("%Y-%m-%d")

        res = self.task_manager.query_global_market_cap(
            asofdate=today, 
            mktcap_thres=mktcap_thres, 
            country=country, 
            allow_fuzzy=True,
        )

        # keep the most recent marketcap
        res = res.sort_values(by="pricingdate", ascending=False).drop_duplicates(subset="companyid")

        if top_x is not None:
            res = res.sort_values(by="usdmarketcap", ascending=False).head(top_x)

        return [MarketCapEntry(
            companyid=row["companyid"],
            marketcap=row["marketcap"],
            pricingdate=row["pricingdate"].strftime("%Y-%m-%d"),
            usdmarketcap=row["usdmarketcap"],
            companyname=row["companyname"],
            tickersymbol=row["tickersymbol"],
            currency=row["currency"],
            exchange=row["exchange"],
            country=row["country"]
            ) for _, row in res.iterrows()]

    def get_historical_market_cap(self, country: str, mktcap: str, year: int, month:int, top_x: int | None = None) -> list[MarketCapEntry]:
        """
        Get the historical market cap for a given country and market cap category
        """
        mktcap_thres = convert_mktcap_to_number(mktcap)

        # get historical market cap
        historical_date = datetime(year, month, 1).strftime("%Y-%m-%d")

        #TODO cache data if it does not exist
        #TODO if it exists, load from cache

        res = self.task_manager.query_global_market_cap(asofdate=historical_date, mktcap_thres=mktcap_thres, country=country, allow_fuzzy=True)

        # keep the most recent marketcap
        res = res.sort_values(by="pricingdate", ascending=False).drop_duplicates(subset="companyid")

        if top_x is not None:
            res = res.sort_values(by="usdmarketcap", ascending=False).head(top_x)

        return [MarketCapEntry(
            companyid=row["companyid"],
            marketcap=row["marketcap"],
            pricingdate=row["pricingdate"].strftime("%Y-%m-%d"),
            usdmarketcap=row["usdmarketcap"],
            companyname=row["companyname"],
            tickersymbol=row["tickersymbol"],
            currency=row["currency"],
            exchange=row["exchange"],
            country=row["country"]
            ) for _, row in res.iterrows()]