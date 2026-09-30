from backend.agents import OptionsAgent
from backend.models import Direction,OptionCandidate

def test_options_agent_prefers_tight_delta_candidate():
    cs=[
      OptionCandidate(symbol="QQQ261002P00740000",option_type="put",expiration="2026-10-02",strike=740,bid=2.00,ask=2.10,delta=-.54,iv=.22),
      OptionCandidate(symbol="QQQ261002P00739000",option_type="put",expiration="2026-10-02",strike=739,bid=1.80,ask=2.20,delta=-.55,iv=.23)]
    signal,selected=OptionsAgent().analyze(cs,Direction.bearish)
    assert selected.symbol=="QQQ261002P00740000"
    assert signal.evidence["eligible"]==1
