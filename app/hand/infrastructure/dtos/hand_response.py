from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from uuid import UUID


class LastPhaseHeroFolded(str, Enum):
    PRE_FLOP = "PRE_FLOP"
    FLOP = "FLOP"
    TURN = "TURN"
    RIVER = "RIVER"

class PotType(str, Enum):
    UNOPENED = "UNOPENED"
    LIMPED = "LIMPED"
    OPEN_RAISED = "OPEN_RAISED"
    ROL_RAISED = "ROL_RAISED"
    THREE_BET = "3BET"
    SQUEEZE = "SQUEEZE"
    FOUR_BET = "4BET"

class GeneralInfo(BaseModel):
    room_hand_id: str
    datetime: str
    game_type: str
    currency: str
    small_blind: float
    big_blind: float
    game: str

class Player(BaseModel):
    seat: int
    name: str
    stack: float

class Action(BaseModel):
    phase: str
    player: str
    action: str
    amount: Optional[float] = None  
    cards: List[str] = []

class PlayerAction(BaseModel):
    seat: int
    name: str
    details: str
    amount: float

class SummaryPlayerResult(BaseModel):
    seat: int
    name: str
    cards: list
    amount: float

class Summary(BaseModel):
    pot: float
    rake: float
    winner: SummaryPlayerResult
    looser: Optional[SummaryPlayerResult]
    community_cards: List[str]
    showdown: bool
    last_phase_hero_folded: LastPhaseHeroFolded
    pot_type: PotType
    hero_seat: int

class Showdown(BaseModel):
    winner: str
    winner_hand: List[str]
    winner_hand_description: str

class FinishBeforeShowdown(BaseModel):
    player: str 
    action: str 
    amount: float

class HandResponseDto(BaseModel):
    id: UUID
    user_id: str
    general_info: GeneralInfo
    players: List[Player]
    hero_cards: List[str]
    hero_name: str
    hero_seat: int
    actions: List[Action]
    summary: Summary 
    table_name: str 
    table_type: str
    button_seat: int
    # showdown: Showdown
    # finish_before_showdown: List[FinishBeforeShowdown]  

class GetHandResponseDto(BaseModel):
    hand: HandResponseDto 
    prev_hand_id: Optional[str]
    next_hand_id: Optional[str]