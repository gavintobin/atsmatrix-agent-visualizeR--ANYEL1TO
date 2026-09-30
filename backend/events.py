import asyncio
from datetime import datetime, timezone
from typing import Any

class EventBus:
    def __init__(self):
        self._subscribers:set[asyncio.Queue]=set()
        self._history:list[dict[str,Any]]=[]

    def subscribe(self):
        q=asyncio.Queue(maxsize=100)
        self._subscribers.add(q)
        return q

    def unsubscribe(self,q):
        self._subscribers.discard(q)

    async def publish(self,event:dict[str,Any]):
        payload={"timestamp":datetime.now(timezone.utc).isoformat(),**event}
        self._history.append(payload);self._history=self._history[-100:]
        for q in list(self._subscribers):
            if q.full():
                try:q.get_nowait()
                except asyncio.QueueEmpty:pass
            await q.put(payload)
        return payload

    @property
    def history(self):return list(self._history)

event_bus=EventBus()
