
from pydantic import BaseModel


class MarketCapEntry(BaseModel):
    """
    sample:
          companyid       marketcap pricingdate usdmarketcap                companyname tickersymbol currency  exchange
0         21835  3235237.693557  2025-05-03   3235237.69      Microsoft Corporation         MSFT      USD  NasdaqGS
1         24937  3067071.869100  2025-05-03   3067071.87                 Apple Inc.         AAPL      USD  NasdaqGS
2         32307  2793800.000000  2025-05-03   2793800.00         NVIDIA Corporation         NVDA      USD  NasdaqGS
3         18749  2016894.630281  2025-05-03   2016894.63           Amazon.com, Inc.         AMZN      USD  NasdaqGS
4         29096  2000221.070000  2025-05-03   2000221.07              Alphabet Inc.        GOOGL      USD  NasdaqGS
    """
    companyid: int
    marketcap: float
    pricingdate: str
    usdmarketcap: float
    companyname: str
    tickersymbol: str
    currency: str
    exchange: str
    country: str