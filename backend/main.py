from pathlib import Path
from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.responses import FileResponse
from pydantic import BaseModel,Field
from backend.config import get_settings
from backend.events import event_bus
from backend.models import OptionCandidate
from backend.alpaca_market import AlpacaMarketData
from backend.market_indicators import build_market_snapshot
from backend.agents import MarketAgent,OptionsAgent
from backend.alpaca_options import AlpacaOptionsData
from backend.orchestrator import TradingOrchestrator

app=FastAPI(title="ATSMATRIX Alpaca QQQ Paper Trader",version="0.2.0")
ROOT=Path(__file__).resolve().parents[1]

class CycleRequest(BaseModel):
    market_snapshot:dict=Field(default_factory=dict)
    news_snapshot:dict=Field(default_factory=dict)
    option_candidates:list[OptionCandidate]=Field(default_factory=list)
    open_positions:int=0
    daily_pnl:float=0

@app.get("/")
def dashboard():return FileResponse(ROOT/"index.html")

@app.get("/health")
def health():
    s=get_settings()
    return {"status":"ok","broker":"alpaca","mode":"paper","trading_enabled":s.trading_enabled,
            "symbol":s.symbol,"option_feed":s.alpaca_option_feed}

@app.get("/api/v1/market/qqq")
async def qqq_market():
    s=get_settings()
    await event_bus.publish({"type":"agent","agent":"market","status":"ANALYZING","message":"Fetching QQQ minute bars from Alpaca"})
    snapshot=build_market_snapshot(AlpacaMarketData(s).bars())
    signal=MarketAgent().analyze(snapshot)
    await event_bus.publish({"type":"agent","agent":"market","status":"COMPLETE","message":signal.summary,
      "data":{"direction":signal.direction.value,"confidence":signal.confidence,**signal.evidence}})
    return {"symbol":s.symbol,"feed":s.alpaca_stock_feed,"snapshot":snapshot,"signal":signal}

@app.get("/api/v1/options/qqq")
async def qqq_options():
    s=get_settings()
    await event_bus.publish({"type":"agent","agent":"options","status":"SCANNING","message":"Fetching QQQ option chain from Alpaca"})
    snapshot=build_market_snapshot(AlpacaMarketData(s).bars())
    market=MarketAgent().analyze(snapshot)
    if market.direction.value=="NEUTRAL":
        signal,selected=OptionsAgent().analyze([],market.direction)
        return {"symbol":s.symbol,"feed":s.alpaca_option_feed,"market_signal":market,"signal":signal,"selected":selected}
    candidates=AlpacaOptionsData(s).candidates(snapshot["price"],market.direction.value)
    signal,selected=OptionsAgent().analyze(candidates,market.direction)
    await event_bus.publish({"type":"agent","agent":"options","status":"COMPLETE","message":signal.summary,
      "data":{"direction":signal.direction.value,"confidence":signal.confidence,**signal.evidence}})
    return {"symbol":s.symbol,"feed":s.alpaca_option_feed,"market_signal":market,
      "contracts_scanned":len(candidates),"signal":signal,"selected":selected}

@app.get("/api/v1/events")
def events():return {"events":event_bus.history}

@app.post("/api/v1/cycle")
async def cycle(q:CycleRequest):
    async def emit(event):await event_bus.publish(event)
    engine=TradingOrchestrator(get_settings(),emit=emit)
    return await engine.run_cycle(market_snapshot=q.market_snapshot,news_snapshot=q.news_snapshot,
      option_candidates=q.option_candidates,open_positions=q.open_positions,daily_pnl=q.daily_pnl)

@app.websocket("/ws")
async def websocket_endpoint(ws:WebSocket):
    await ws.accept();q=event_bus.subscribe()
    try:
        await ws.send_json({"type":"system","agent":"orchestrator","status":"CONNECTED","message":"ATSMATRIX backend connected"})
        for event in event_bus.history[-20:]:await ws.send_json(event)
        while True:await ws.send_json(await q.get())
    except (WebSocketDisconnect,RuntimeError):
        pass
    finally:event_bus.unsubscribe(q)
