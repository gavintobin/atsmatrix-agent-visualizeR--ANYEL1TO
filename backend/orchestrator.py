from backend.agents import MarketAgent,NewsAgent,OptionsAgent,StrategyAgent
from backend.execution import AlpacaPaperExecutor
from backend.models import CycleResult
from backend.risk import RiskEngine

class TradingOrchestrator:
    def __init__(self,s,emit=None):
        self.market=MarketAgent();self.news=NewsAgent();self.options=OptionsAgent()
        self.strategy=StrategyAgent();self.risk=RiskEngine(s);self.executor=AlpacaPaperExecutor(s)
        self.emit=emit

    async def _event(self,agent,status,message,**data):
        if self.emit:await self.emit({"type":"agent","agent":agent,"status":status,"message":message,"data":data})

    async def run_cycle(self,*,market_snapshot,news_snapshot,option_candidates,open_positions=0,daily_pnl=0):
        await self._event("orchestrator","RUNNING","Trading cycle started")
        await self._event("market","ANALYZING","Evaluating QQQ technical state")
        m=self.market.analyze(market_snapshot)
        await self._event("market","COMPLETE",m.summary,direction=m.direction.value,confidence=m.confidence,**m.evidence)

        await self._event("news","ANALYZING","Evaluating supplied news/catalyst snapshot")
        n=self.news.analyze(news_snapshot)
        await self._event("news","COMPLETE",n.summary,direction=n.direction.value,confidence=n.confidence,**n.evidence)

        await self._event("options","SCANNING",f"Scanning {len(option_candidates)} option candidates")
        o,c=self.options.analyze(option_candidates,m.direction)
        await self._event("options","COMPLETE",o.summary,direction=o.direction.value,confidence=o.confidence,
                          contract=c.model_dump() if c else None)

        ss=[m,n,o]
        await self._event("strategy","SYNTHESIZING","Combining agent signals")
        p=self.strategy.synthesize(ss,c)
        await self._event("strategy","COMPLETE","Trade proposal created" if p else "No-trade decision",
                          direction=p.direction.value if p else "NONE",confidence=p.confidence if p else 0)

        r=self.risk.evaluate(p,open_positions=open_positions,daily_pnl=daily_pnl)
        await self._event("risk","APPROVED" if r.approved else "REJECTED","; ".join(r.reasons),approved=r.approved)

        e=None
        if r.approved and p:
            await self._event("execution","SUBMITTING","Sending risk-approved order to Alpaca paper executor")
            e=self.executor.submit(p,r)
            await self._event("execution",e.get("status","UNKNOWN"),"Alpaca paper execution result",**e)
        else:
            await self._event("execution","IDLE","No order submitted")

        await self._event("orchestrator","COMPLETE","Trading cycle completed")
        return CycleResult(signals=ss,proposal=p,risk=r,execution=e)
