from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from alpaca.data.enums import OptionsFeed
from alpaca.data.historical.option import OptionHistoricalDataClient
from alpaca.data.requests import OptionChainRequest
from alpaca.trading.enums import ContractType
from backend.models import OptionCandidate

NY=ZoneInfo("America/New_York")

def _occ(symbol:str):
    tail=symbol[-15:]; expiration=f"20{tail[:2]}-{tail[2:4]}-{tail[4:6]}"
    return ("call" if tail[6]=="C" else "put",expiration,int(tail[7:])/1000)

class AlpacaOptionsData:
    def __init__(self,settings):
        if not settings.alpaca_api_key or not settings.alpaca_secret_key:
            raise RuntimeError("Set ALPACA_API_KEY and ALPACA_SECRET_KEY in .env")
        self.settings=settings
        self.client=OptionHistoricalDataClient(settings.alpaca_api_key,settings.alpaca_secret_key)

    def candidates(self,underlying_price:float,direction:str):
        today=datetime.now(NY).date();kind="call" if direction=="BULLISH" else "put"
        feed=OptionsFeed(self.settings.alpaca_option_feed.lower())
        req=OptionChainRequest(underlying_symbol=self.settings.symbol,feed=feed,
            type=ContractType.CALL if kind=="call" else ContractType.PUT,
            expiration_date_gte=today,expiration_date_lte=today+timedelta(days=7),
            strike_price_gte=round(underlying_price*.97,2),strike_price_lte=round(underlying_price*1.03,2))
        chain=self.client.get_option_chain(req);out=[]
        for symbol,snap in chain.items():
            q=getattr(snap,"latest_quote",None)
            if not q:continue
            bid=float(q.bid_price or 0);ask=float(q.ask_price or 0)
            if bid<=0 or ask<bid:continue
            option_type,expiration,strike=_occ(symbol)
            g=getattr(snap,"greeks",None);delta=float(g.delta) if g and g.delta is not None else None
            iv=float(snap.implied_volatility) if getattr(snap,"implied_volatility",None) is not None else None
            out.append(OptionCandidate(symbol=symbol,underlying=self.settings.symbol,option_type=option_type,
                expiration=expiration,strike=strike,bid=bid,ask=ask,delta=delta,iv=iv))
        return out
