import asyncio
from backend.config import Settings
from backend.models import OptionCandidate
from backend.orchestrator import TradingOrchestrator

def test_dry_run():
    events=[]
    async def emit(e):events.append(e)
    e=TradingOrchestrator(Settings(trading_enabled=False),emit=emit)
    o=OptionCandidate(symbol="QQQ261016C00600000",option_type="call",expiration="2026-10-16",strike=600,bid=2,ask=2.08,delta=.55)
    r=asyncio.run(e.run_cycle(market_snapshot={"price":602,"vwap":600,"orb_high":601,"orb_low":596,"relative_volume":1.4},
      news_snapshot={"sentiment":.3},option_candidates=[o]))
    assert r.risk.approved and r.execution["status"]=="DRY_RUN"
    assert {x["agent"] for x in events}>={"market","news","options","strategy","risk","execution","orchestrator"}
