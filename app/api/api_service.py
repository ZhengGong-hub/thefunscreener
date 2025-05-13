from datetime import datetime
from app.database.db_task_manager import TaskManagerRepository
from app.utils.logging import get_logger

from app.models.marketcap import MarketCapEntry


logger = get_logger(__name__)

class TheFunScreenerService:
    def __init__(self, task_manager: TaskManagerRepository):
        self.task_manager = task_manager


    def get_latest_market_cap(self, country: str, mktcap: str) -> list[MarketCapEntry]:
        """
        Get the latest market cap for a given country and market cap category

        Args:
            country: The country to get the market cap for
            mktcap: The market cap category, can take values "mega", "large", "mid"

        Returns:
            list[MarketCapEntry]: A list of market cap entries
        """

        # convert mktcap from caategories to number
        if mktcap == "mega":
            mktcap_thres = 200e3 # 200 billion
        elif mktcap == "large":
            mktcap_thres = 10e3 # 10 billion
        elif mktcap == "mid":
            mktcap_thres = 2e3 # 2 billion
        else:
            raise ValueError(f"Invalid market cap category: {mktcap}")

        # get the latest trading date
        today = datetime.now().strftime("%Y-%m-%d")

        res = self.task_manager.query_global_market_cap(asofdate=today, mktcap_thres=mktcap_thres, country=country, allow_fuzzy=True)

        # keep the most recent marketcap
        res = res.sort_values(by="pricingdate", ascending=False).drop_duplicates(subset="companyid")

        return [MarketCapEntry(
            companyid=row["companyid"],
            marketcap=row["marketcap"],
            pricingdate=row["pricingdate"].strftime("%Y-%m-%d"),
            usdmarketcap=row["usdmarketcap"],
            companyname=row["companyname"],
            tickersymbol=row["tickersymbol"],
            currency=row["currency"],
            exchange=row["exchange"]
            ) for _, row in res.iterrows()]
