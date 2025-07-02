from pydantic import BaseModel
from typing import List


class PlayerStatsResponse(BaseModel):
    name: str
    hands: int
    # fold: int
    # limp: int
    # open_raise: int
    # rol: int
    # three_bet: int
    # squeeze: int
    # four_bet: int
    # call_to_or: int
    # call_to_rol: int
    # call_to_3bet: int
    # call_to_squeeze: int
    # call_to_4bet: int
    # fold_to_3bet: int
    # fold_to_squeeze: int
    # fold_to_4bet: int
    # three_bet_opp: int
    vpip: float
    pfr: float
    three_bet_percent: float
    is_hero: bool


GenerateStatsResponse = List[PlayerStatsResponse]
