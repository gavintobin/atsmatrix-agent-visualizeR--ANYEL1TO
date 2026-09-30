from types import SimpleNamespace
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from backend.agents import MarketAgent
from backend.market_indicators import build_market_snapshot

NY=ZoneInfo("America/New_York")
def bar(ts,o,h,l,c,v):
    return SimpleNamespace(timestamp=ts,open=o,high=h,low=l,close=c,volume=v,vwap=c)

def test_snapshot_and_bullish_signal():
    start=datetime(2026,9,30,9,30,tzinfo=NY)
    bars=[bar(start+timedelta(minutes=i),600+i*.1,600.2+i*.1,599.9+i*.1,600.1+i*.1,1000+i*10) for i in range(30)]
    snap=build_market_snapshot(bars)
    assert snap["orb_high"]>snap["orb_low"]
    assert snap["vwap"]>0
    assert snap["bars"]==30
    sig=MarketAgent().analyze(snap)
    assert sig.agent=="market"
    assert 0<=sig.confidence<=1
