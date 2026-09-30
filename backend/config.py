from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    alpaca_api_key:str=""; alpaca_secret_key:str=""; alpaca_paper:bool=True
    trading_enabled:bool=False; symbol:str="QQQ"; alpaca_stock_feed:str="iex"; alpaca_option_feed:str="indicative"
    max_contracts_per_trade:int=1; max_open_positions:int=1; max_daily_loss_usd:float=100
    min_signal_confidence:float=.70; max_option_spread_pct:float=.08
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    def assert_safe(self):
        if not self.alpaca_paper: raise RuntimeError("Starter is paper-only.")
@lru_cache
def get_settings():
    s=Settings(); s.assert_safe(); return s
