from backend.agents import MarketAgent,NewsAgent,OptionsAgent,StrategyAgent
from backend.execution import AlpacaPaperExecutor
from backend.models import CycleResult
from backend.risk import RiskEngine
class TradingOrchestrator:
    def __init__(self,s):
        self.market=MarketAgent();self.news=NewsAgent();self.options=OptionsAgent();self.strategy=StrategyAgent();self.risk=RiskEngine(s);self.executor=AlpacaPaperExecutor(s)
    def run_cycle(self,*,market_snapshot,news_snapshot,option_candidates,open_positions=0,daily_pnl=0):
        m=self.market.analyze(market_snapshot);n=self.news.analyze(news_snapshot);o,c=self.options.analyze(option_candidates,m.direction)
        ss=[m,n,o];p=self.strategy.synthesize(ss,c);r=self.risk.evaluate(p,open_positions=open_positions,daily_pnl=daily_pnl)
        e=self.executor.submit(p,r) if r.approved and p else None
        return CycleResult(signals=ss,proposal=p,risk=r,execution=e)
