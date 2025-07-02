from typing import Dict, List, Union
from dataclasses import dataclass


@dataclass
class PlayerStats:
    name: str = ""
    hands: int = 0
    fold: int = 0
    limp: int = 0
    open_raise: int = 0
    rol: int = 0
    three_bet: int = 0
    squeeze: int = 0
    four_bet: int = 0
    call_to_or: int = 0
    call_to_rol: int = 0
    call_to_3bet: int = 0
    call_to_squeeze: int = 0
    call_to_4bet: int = 0
    fold_to_3bet: int = 0
    fold_to_squeeze: int = 0
    fold_to_4bet: int = 0
    three_bet_opp: int = 0
    vpip: float = 0.0
    pfr: float = 0.0
    three_bet_percent: float = 0.0
    is_hero: bool = False

    def set_att(self, att_name: str, val: Union[float, int]):
        if not hasattr(self, att_name):
            raise ValueError(f"Unknown Attribute: {att_name}")
        setattr(self, att_name, val)

    def increment(self, stat_name: str):
        if not hasattr(self, stat_name):
            raise ValueError(f"Unknown stat: {stat_name}")
        setattr(self, stat_name, getattr(self, stat_name) + 1)

    def to_primitives(self) -> Dict:
        """Convert the PlayerStats instance to a dictionary."""
        return self.__dict__


class Stats:
    def __init__(self, user_id: str, players_stats: List[PlayerStats]) -> None:
        self.user_id = user_id
        self.players_stats = players_stats

    @staticmethod
    def create(user_id: str, players_stats: List[PlayerStats]):
        return Stats(user_id, players_stats)

    def to_primitives(self) -> Dict:
        return {
            "user_id": self.user_id,
            "players": [p.to_primitives() for p in self.players_stats],
        }
