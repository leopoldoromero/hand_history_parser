from pydantic import BaseModel
from typing import List
from app.hand.domain.hand import Hand, GeneralInfo, Player, Action, Summary


class HandSchema(BaseModel):
    id: str
    general_info: GeneralInfo
    table_name: str
    table_type: str
    button_seat: int
    players: List[Player]
    hero_cards: List[str]
    hero_name: str
    hero_seat: int
    actions: List[Action]
    summary: Summary

    class Config:
        orm_mode = True

    @staticmethod
    def from_domain(hand: Hand) -> "HandSchema":
        """Creates a HandSchema instance from a domain Hand instance."""
        return HandSchema(
            id=hand.id,
            general_info=hand.general_info,
            table_name=hand.table_name,
            table_type=hand.table_type,
            button_seat=hand.button_seat,
            players=hand.players,
            hero_cards=hand.hero_cards,
            hero_name=hand.hero_name,
            hero_seat=hand.hero_seat,
            actions=hand.actions,
            summary=hand.summary
        )
