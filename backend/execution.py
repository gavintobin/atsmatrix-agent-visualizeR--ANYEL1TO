class AlpacaPaperExecutor:
    def __init__(self,s):self.s=s;s.assert_safe()
    def submit(self,p,r):
        if not r.approved or p.option is None:raise ValueError("Order is not risk-approved.")
        payload={"symbol":p.option.symbol,"qty":p.quantity,"side":"buy","type":"limit","time_in_force":"day","limit_price":round(p.option.ask,2)}
        if not self.s.trading_enabled:return {"status":"DRY_RUN","order":payload}
        if not self.s.alpaca_api_key or not self.s.alpaca_secret_key:raise RuntimeError("Alpaca paper credentials required.")
        from alpaca.trading.client import TradingClient
        from alpaca.trading.enums import OrderSide,TimeInForce
        from alpaca.trading.requests import LimitOrderRequest
        client=TradingClient(self.s.alpaca_api_key,self.s.alpaca_secret_key,paper=True)
        o=client.submit_order(order_data=LimitOrderRequest(symbol=p.option.symbol,qty=p.quantity,side=OrderSide.BUY,time_in_force=TimeInForce.DAY,limit_price=round(p.option.ask,2)))
        return {"status":str(o.status),"order_id":str(o.id),"symbol":o.symbol}
