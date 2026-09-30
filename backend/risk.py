from backend.models import RiskDecision
class RiskEngine:
    def __init__(self,s):self.s=s
    def evaluate(self,p,*,open_positions=0,daily_pnl=0):
        if p is None:return RiskDecision(approved=False,reasons=["No trade proposal."])
        r=[]
        if p.underlying!=self.s.symbol:r.append("Only configured underlying is allowed.")
        if p.confidence<self.s.min_signal_confidence:r.append("Signal confidence below threshold.")
        if p.quantity<1 or p.quantity>self.s.max_contracts_per_trade:r.append("Contract quantity exceeds limit.")
        if open_positions>=self.s.max_open_positions:r.append("Maximum open positions reached.")
        if daily_pnl<=-self.s.max_daily_loss_usd:r.append("Daily loss kill switch is active.")
        if p.option is None:r.append("No option contract selected.")
        elif p.option.spread_pct>self.s.max_option_spread_pct:r.append("Option spread exceeds limit.")
        return RiskDecision(approved=not r,reasons=r or ["All hard risk checks passed."])
