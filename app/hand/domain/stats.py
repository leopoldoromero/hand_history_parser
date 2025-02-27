from typing import Dict
from dataclasses import dataclass


@dataclass
class PlayerStats:
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

    def to_primitives(self) -> Dict:
        """Convert the PlayerStats instance to a dictionary."""
        return {attr: getattr(self, attr) for attr in self.__dict__}


class Stats(Dict[str, PlayerStats]):
    def to_primitives(self) -> Dict[str, Dict]:
        """Convert the entire Stats dictionary to a primitive dictionary."""
        return {user: stats.to_primitives() for user, stats in self.items()}
