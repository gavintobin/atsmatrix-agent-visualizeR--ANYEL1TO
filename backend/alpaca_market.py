from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from alpaca.data.enums import DataFeed
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

NY=ZoneInfo("America/New_York")

class AlpacaMarketData:
    def __init__(self,settings):
        if not settings.alpaca_api_key or not settings.alpaca_secret_key:
            raise RuntimeError("Set ALPACA_API_KEY and ALPACA_SECRET_KEY in .env")
        self.settings=settings
        self.client=StockHistoricalDataClient(settings.alpaca_api_key,settings.alpaca_secret_key)

    def bars(self,lookback_days:int=10):
        now=datetime.now(NY)
        req=StockBarsRequest(symbol_or_symbols=[self.settings.symbol],
            timeframe=TimeFrame(1,TimeFrameUnit.Minute),
            start=now-timedelta(days=lookback_days),end=now,
            feed=DataFeed(self.settings.alpaca_stock_feed.lower()))
        result=self.client.get_stock_bars(req)
        return list(result[self.settings.symbol])
