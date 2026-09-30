from fastapi import FastAPI
from pydantic import BaseModel,Field
from backend.config import get_settings
from backend.models import OptionCandidate
from backend.orchestrator import TradingOrchestrator
app=FastAPI(title="ATSMATRIX Alpaca QQQ Paper Trader",version="0.1.0")
class CycleRequest(BaseModel):
    market_snapshot:dict=Field(default_factory=dict);news_snapshot:dict=Field(default_factory=dict)
    option_candidates:list[OptionCandidate]=Field(default_factory=list);open_positions:int=0;daily_pnl:float=0
@app.get("/health")
def health():
    s=get_settings();return {"status":"ok","broker":"alpaca","mode":"paper","trading_enabled":s.trading_enabled,"symbol":s.symbol,"option_feed":s.alpaca_option_feed}
@app.post("/api/v1/cycle")
def cycle(q:CycleRequest):
    return TradingOrchestrator(get_settings()).run_cycle(market_snapshot=q.market_snapshot,news_snapshot=q.news_snapshot,option_candidates=q.option_candidates,open_positions=q.open_positions,daily_pnl=q.daily_pnl)
