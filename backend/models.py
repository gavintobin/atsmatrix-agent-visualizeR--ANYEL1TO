from enum import Enum
from typing import Any
from pydantic import BaseModel,Field
class Direction(str,Enum): bullish="BULLISH"; bearish="BEARISH"; neutral="NEUTRAL"
class AgentSignal(BaseModel):
    agent:str; direction:Direction=Direction.neutral; confidence:float=Field(ge=0,le=1); summary:str
    evidence:dict[str,Any]=Field(default_factory=dict)
class OptionCandidate(BaseModel):
    symbol:str; underlying:str="QQQ"; option_type:str; expiration:str; strike:float; bid:float; ask:float
    delta:float|None=None; iv:float|None=None
    @property
    def spread_pct(self):
        mid=(self.bid+self.ask)/2; return (self.ask-self.bid)/mid if mid>0 else 1.
class TradeProposal(BaseModel):
    underlying:str="QQQ"; direction:Direction; confidence:float=Field(ge=0,le=1)
    option:OptionCandidate|None=None; quantity:int=1; rationale:list[str]=Field(default_factory=list)
class RiskDecision(BaseModel): approved:bool; reasons:list[str]=Field(default_factory=list)
class CycleResult(BaseModel):
    signals:list[AgentSignal]; proposal:TradeProposal|None; risk:RiskDecision; execution:dict[str,Any]|None=None
