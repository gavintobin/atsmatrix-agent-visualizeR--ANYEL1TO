from backend.config import Settings
from backend.models import Direction,OptionCandidate,TradeProposal
from backend.risk import RiskEngine
def p(spread=.04):
    bid=2.;ask=bid*(2+spread)/(2-spread);o=OptionCandidate(symbol="QQQ261016C00600000",option_type="call",expiration="2026-10-16",strike=600,bid=bid,ask=ask,delta=.55)
    return TradeProposal(direction=Direction.bullish,confidence=.8,option=o)
def test_approve():assert RiskEngine(Settings()).evaluate(p()).approved
def test_spread():assert not RiskEngine(Settings()).evaluate(p(.2)).approved
def test_kill():assert not RiskEngine(Settings(max_daily_loss_usd=100)).evaluate(p(),daily_pnl=-100).approved
