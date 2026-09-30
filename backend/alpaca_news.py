from datetime import datetime,timedelta,timezone
from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import NewsRequest

# QQQ plus large index constituents that often drive index-level headlines.
DEFAULT_SYMBOLS=["QQQ","NVDA","AAPL","MSFT","AMZN","META","AVGO","GOOGL","TSLA"]

class AlpacaNewsData:
    def __init__(self,settings):
        if not settings.alpaca_api_key or not settings.alpaca_secret_key:
            raise RuntimeError("Set ALPACA_API_KEY and ALPACA_SECRET_KEY in .env")
        self.client=NewsClient(settings.alpaca_api_key,settings.alpaca_secret_key)

    def recent(self,hours:int=12,limit:int=50):
        end=datetime.now(timezone.utc);start=end-timedelta(hours=hours)
        req=NewsRequest(symbols=",".join(DEFAULT_SYMBOLS),start=start,end=end,limit=limit,sort="desc")
        result=self.client.get_news(req)
        articles=getattr(result,"news",result)
        out=[]
        for a in articles:
            out.append({"id":getattr(a,"id",None),"headline":getattr(a,"headline",""),
              "summary":getattr(a,"summary",""),"symbols":list(getattr(a,"symbols",[]) or []),
              "created_at":str(getattr(a,"created_at","")),"source":getattr(a,"source","")})
        return out
