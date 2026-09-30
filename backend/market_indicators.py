from collections import defaultdict
from datetime import time
from zoneinfo import ZoneInfo

NY=ZoneInfo("America/New_York")

def _rsi(closes,period=14):
    if len(closes)<=period:return None
    changes=[closes[i]-closes[i-1] for i in range(1,len(closes))]
    gains=[max(x,0) for x in changes[-period:]];losses=[max(-x,0) for x in changes[-period:]]
    avg_gain=sum(gains)/period;avg_loss=sum(losses)/period
    if avg_loss==0:return 100.0
    rs=avg_gain/avg_loss
    return 100-(100/(1+rs))

def build_market_snapshot(bars):
    regular=[]
    for b in bars:
        ts=b.timestamp.astimezone(NY)
        if time(9,30)<=ts.time()<time(16,0):regular.append((ts,b))
    if not regular:raise RuntimeError("No regular-session QQQ bars returned by Alpaca")

    by_day=defaultdict(list)
    for ts,b in regular:by_day[ts.date()].append((ts,b))
    days=sorted(by_day)
    current=by_day[days[-1]]
    price=float(current[-1][1].close)

    pv=sum(float(b.vwap if b.vwap is not None else b.close)*float(b.volume) for _,b in current)
    vol=sum(float(b.volume) for _,b in current)
    vwap=pv/vol if vol else price

    opening=[b for ts,b in current if time(9,30)<=ts.time()<time(9,35)]
    orb_high=max(float(b.high) for b in opening) if opening else price
    orb_low=min(float(b.low) for b in opening) if opening else price

    minute_count=len(current)
    current_volume=sum(float(b.volume) for _,b in current)
    prior=[]
    for d in days[:-1][-5:]:
        comparable=by_day[d][:minute_count]
        if comparable:prior.append(sum(float(b.volume) for _,b in comparable))
    avg_prior=sum(prior)/len(prior) if prior else current_volume
    relative_volume=current_volume/avg_prior if avg_prior else 1.0

    closes=[float(b.close) for _,b in current]
    rsi=_rsi(closes)
    momentum_5=(price/closes[-6]-1) if len(closes)>=6 and closes[-6] else 0.0
    return {"price":price,"vwap":vwap,"orb_high":orb_high,"orb_low":orb_low,
            "relative_volume":relative_volume,"rsi":rsi,"momentum_5m":momentum_5,
            "session_volume":current_volume,"bars":minute_count,
            "session_date":str(days[-1])}
