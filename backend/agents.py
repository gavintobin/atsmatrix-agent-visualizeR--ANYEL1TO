from statistics import mean
from backend.models import AgentSignal,Direction,OptionCandidate,TradeProposal
class MarketAgent:
    def analyze(self,s):
        p=float(s.get("price",0));v=float(s.get("vwap",p));hi=float(s.get("orb_high",p));lo=float(s.get("orb_low",p));rv=float(s.get("relative_volume",1))
        d,b=(Direction.bullish,.72) if p>hi and p>v else (Direction.bearish,.72) if p<lo and p<v else (Direction.neutral,.45)
        return AgentSignal(agent="market",direction=d,confidence=min(.95,b+max(0,rv-1)*.05),summary=f"QQQ technical state: {d.value}",evidence={"price":p,"vwap":v,"orb_high":hi,"orb_low":lo,"relative_volume":rv})
class NewsAgent:
    def analyze(self,n):
        x=float(n.get("sentiment",0));d=Direction.bullish if x>=.2 else Direction.bearish if x<=-.2 else Direction.neutral
        return AgentSignal(agent="news",direction=d,confidence=min(.9,.5+abs(x)*.4),summary=n.get("summary","No material news catalyst supplied."),evidence={"sentiment":x,"headlines":n.get("headlines",[])[:10]})
class OptionsAgent:
    def analyze(self,cs:list[OptionCandidate],d:Direction):
        want="call" if d==Direction.bullish else "put";valid=[c for c in cs if c.option_type.lower()==want and c.bid>0 and c.ask>=c.bid]
        if not valid or d==Direction.neutral:return AgentSignal(agent="options",confidence=.3,summary="No suitable option candidate."),None
        c=min(valid,key=lambda x:(x.spread_pct,abs((x.delta if x.delta is not None else .55)-.55)))
        return AgentSignal(agent="options",direction=d,confidence=max(.3,min(.95,1-c.spread_pct*3)),summary=f"Selected {c.symbol}.",evidence={"spread_pct":c.spread_pct}),c
class StrategyAgent:
    def synthesize(self,ss,option):
        ds=[s for s in ss if s.direction!=Direction.neutral]
        if not ds or option is None:return None
        bull=sum(s.confidence for s in ds if s.direction==Direction.bullish);bear=sum(s.confidence for s in ds if s.direction==Direction.bearish)
        d=Direction.bullish if bull>bear else Direction.bearish;a=[s for s in ds if s.direction==d]
        return TradeProposal(direction=d,confidence=mean(s.confidence for s in a),option=option,rationale=[f"{s.agent}: {s.summary}" for s in a])
