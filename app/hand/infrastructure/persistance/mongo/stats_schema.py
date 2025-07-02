from pydantic import BaseModel
from typing import List, Optional
from app.hand.domain.stats import PlayerStats
from app.hand.domain.stats import Stats


class PlayerStatsSchema(BaseModel):
    name: str
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

    @staticmethod
    def from_domain(player_stats: PlayerStats) -> "PlayerStatsSchema":
        return PlayerStatsSchema(
            name=player_stats.name,
            hands=player_stats.hands,
            fold=player_stats.fold,
            limp=player_stats.limp,
            open_raise=player_stats.open_raise,
            rol=player_stats.rol,
            three_bet=player_stats.three_bet,
            squeeze=player_stats.squeeze,
            four_bet=player_stats.four_bet,
            call_to_or=player_stats.call_to_or,
            call_to_rol=player_stats.call_to_rol,
            call_to_3bet=player_stats.call_to_3bet,
            call_to_squeeze=player_stats.call_to_squeeze,
            call_to_4bet=player_stats.call_to_4bet,
            fold_to_3bet=player_stats.fold_to_3bet,
            fold_to_squeeze=player_stats.fold_to_squeeze,
            fold_to_4bet=player_stats.fold_to_4bet,
            three_bet_opp=player_stats.three_bet_opp,
            vpip=player_stats.vpip,
            pfr=player_stats.pfr,
            three_bet_percent=player_stats.three_bet_percent,
            is_hero=player_stats.is_hero,
        )

    def to_domain(self) -> PlayerStats:
        return PlayerStats(
            name=self.name,
            hands=self.hands,
            fold=self.fold,
            limp=self.limp,
            open_raise=self.open_raise,
            rol=self.rol,
            three_bet=self.three_bet,
            squeeze=self.squeeze,
            four_bet=self.four_bet,
            call_to_or=self.call_to_or,
            call_to_rol=self.call_to_rol,
            call_to_3bet=self.call_to_3bet,
            call_to_squeeze=self.call_to_squeeze,
            call_to_4bet=self.call_to_4bet,
            fold_to_3bet=self.fold_to_3bet,
            fold_to_squeeze=self.fold_to_squeeze,
            fold_to_4bet=self.fold_to_4bet,
            three_bet_opp=self.three_bet_opp,
            vpip=self.vpip,
            pfr=self.pfr,
            three_bet_percent=self.three_bet_percent,
            is_hero=self.is_hero,
        )


class StatsSchema(BaseModel):
    user_id: str
    players_stats: List[PlayerStatsSchema]

    @staticmethod
    def from_domain(stats: Stats) -> "StatsSchema":
        """Convert domain Stats object into StatsSchema."""
        return StatsSchema(
            user_id=stats.user_id,
            players_stats=[
                PlayerStatsSchema.from_domain(player_stats)
                for player_stats in stats.players_stats
            ],
        )

    def to_domain(self) -> Optional[Stats]:
        """Convert StatsSchema back to domain Stats object."""
        return Stats.create(
            self.user_id,
            players_stats=[
                player_stats.to_domain() for player_stats in self.players_stats
            ],
        )
