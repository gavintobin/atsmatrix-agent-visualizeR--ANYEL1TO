from backend.config import Settings
from backend.models import OptionCandidate
from backend.orchestrator import TradingOrchestrator
def test_dry_run():
    e=TradingOrchestrator(Settings(trading_enabled=False));o=OptionCandidate(symbol="QQQ261016C00600000",option_type="call",expiration="2026-10-16",strike=600,bid=2,ask=2.08,delta=.55)
    r=e.run_cycle(market_snapshot={"price":602,"vwap":600,"orb_high":601,"orb_low":596,"relative_volume":1.4},news_snapshot={"sentiment":.3},option_candidates=[o])
    assert r.risk.approved and r.execution["status"]=="DRY_RUN"
