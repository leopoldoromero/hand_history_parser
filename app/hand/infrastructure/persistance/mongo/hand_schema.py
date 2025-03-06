from pydantic import BaseModel
from typing import List, Optional
from app.hand.domain.hand import (
    Hand,
    Hero,
    GeneralInfo,
    Player,
    Action,
    Summary,
    SummaryPlayerResult,
)


class HeroSchema(BaseModel):
    nick: str
    cards: List[str]
    seat: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @staticmethod
    def from_domain(hero: Hero) -> "HeroSchema":
        return HeroSchema(nick=hero.nick, cards=hero.cards, seat=hero.seat)

    def to_domain(self) -> Hero:
        return Hero.from_primitives(
            {"nick": self.nick, "cards": self.cards, "seat": self.seat}
        )


class PlayerSchema(BaseModel):
    seat: int
    name: str
    stack: float

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @staticmethod
    def from_domain(player: Player) -> "PlayerSchema":
        return PlayerSchema(seat=player.seat, name=player.name, stack=player.stack)

    def to_domain(self) -> Player:
        return Player.from_primitives(
            {"seat": self.seat, "name": self.name, "stack": self.stack}
        )


class ActionSchema(BaseModel):
    phase: str
    player: str
    action: str
    amount: Optional[float]
    cards: List[str]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @staticmethod
    def from_domain(action: Action) -> "ActionSchema":
        return ActionSchema(
            phase=action.phase,
            player=action.player,
            action=action.action,
            amount=action.amount,
            cards=action.cards,
        )

    def to_domain(self) -> Action:
        return Action.from_primitives(
            {
                "phase": self.phase,
                "player": self.player,
                "action": self.action,
                "amount": self.amount,
                "cards": self.cards,
            }
        )


class GeneralInfoSchema(BaseModel):
    room_hand_id: str
    datetime: str
    game_type: str
    currency: str
    small_blind: float
    big_blind: float
    game: str
    room: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @staticmethod
    def from_domain(info: GeneralInfo) -> "GeneralInfoSchema":
        return GeneralInfoSchema(
            room_hand_id=info.room_hand_id,
            datetime=info.datetime,
            game_type=info.game_type,
            currency=info.currency,
            small_blind=info.small_blind,
            big_blind=info.big_blind,
            game=info.game,
            room=info.room,
        )

    def to_domain(self) -> GeneralInfo:
        return GeneralInfo.from_primitives(
            {
                "room_hand_id": self.room_hand_id,
                "datetime": self.datetime,
                "game_type": self.game_type,
                "currency": self.currency,
                "small_blind": self.small_blind,
                "big_blind": self.big_blind,
                "game": self.game,
                "room": self.room,
            }
        )


class SummaryPlayerResultSchema(BaseModel):
    seat: int
    name: str
    cards: List[str]
    amount: Optional[float]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @staticmethod
    def from_domain(result: SummaryPlayerResult) -> "SummaryPlayerResultSchema":
        return SummaryPlayerResultSchema(
            seat=result.seat, name=result.name, cards=result.cards, amount=result.amount
        )

    def to_domain(self) -> SummaryPlayerResult:
        return SummaryPlayerResult.from_primitives(
            {
                "seat": self.seat,
                "name": self.name,
                "cards": self.cards,
                "amount": self.amount,
            }
        )


class SummarySchema(BaseModel):
    pot: float
    rake: float
    winner: SummaryPlayerResultSchema
    looser: Optional[SummaryPlayerResultSchema]
    community_cards: List[str]
    showdown: bool
    pot_type: str
    last_phase_hero_folded: Optional[str]
    hero_seat: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @staticmethod
    def from_domain(summary: Summary) -> "SummarySchema":
        return SummarySchema(
            pot=summary.pot,
            rake=summary.rake,
            winner=SummaryPlayerResultSchema.from_domain(summary.winner),
            looser=SummaryPlayerResultSchema.from_domain(summary.looser)
            if summary.looser
            else None,
            community_cards=summary.community_cards,
            showdown=summary.showdown,
            pot_type=summary.pot_type,
            last_phase_hero_folded=summary.last_phase_hero_folded,
            hero_seat=summary.hero_seat,
        )

    def to_domain(self) -> Summary:
        return Summary.from_primitives(
            {
                "pot": self.pot,
                "rake": self.rake,
                "winner": {
                    "seat": self.winner.seat,
                    "name": self.winner.name,
                    "cards": self.winner.cards,
                    "amount": self.winner.amount,
                },
                "looser": {
                    "seat": self.looser.seat,
                    "name": self.looser.name,
                    "cards": self.looser.cards,
                    "amount": self.looser.amount,
                }
                if self.looser
                else None,
                "community_cards": self.community_cards,
                "showdown": self.showdown,
                "pot_type": self.pot_type,
                "last_phase_hero_folded": self.last_phase_hero_folded,
                "hero_seat": self.hero_seat,
            }
        )


class HandSchema(BaseModel):
    id: str
    user_id: str
    general_info: GeneralInfoSchema
    table_name: str
    table_type: str
    button_seat: int
    players: List[PlayerSchema]
    hero_cards: List[str]
    hero_name: str
    hero_seat: int
    actions: List[ActionSchema]
    summary: SummarySchema

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @staticmethod
    def from_domain(hand: Hand) -> "HandSchema":
        """Creates a HandSchema instance from a domain Hand instance."""
        return HandSchema(
            id=hand.id,
            user_id=hand.user_id,
            general_info=GeneralInfoSchema.from_domain(hand.general_info),
            table_name=hand.table_name,
            table_type=hand.table_type,
            button_seat=hand.button_seat,
            players=[PlayerSchema.from_domain(player) for player in hand.players],
            hero_cards=hand.hero_cards,
            hero_name=hand.hero_name,
            hero_seat=hand.hero_seat,
            actions=[ActionSchema.from_domain(action) for action in hand.actions],
            summary=SummarySchema.from_domain(hand.summary),
        )

    def to_domain(self) -> "Hand":
        """Creates a domain Hand instance."""
        return Hand(
            self.id,
            self.user_id,
            self.general_info.to_domain(),
            self.table_name,
            self.table_type,
            self.button_seat,
            [player.to_domain() for player in self.players],
            self.hero_cards,
            self.hero_name,
            self.hero_seat,
            [action.to_domain() for action in self.actions],
            self.summary.to_domain(),
        )
