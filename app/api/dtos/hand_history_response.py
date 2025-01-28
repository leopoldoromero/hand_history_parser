from pydantic import BaseModel
from typing import List, Optional

class GeneralInfo(BaseModel):
    hand_id: str
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

class Summary(BaseModel):
    player_actions: List[PlayerAction]
    pot: float
    rake: float

class Showdown(BaseModel):
    winner: str
    winner_hand: List[str]
    winner_hand_description: str

class Hand(BaseModel):
    general_info: GeneralInfo
    players: List[Player]
    hero_hand: List[str]
    actions: List[Action]
    summary: Summary
    showdown: Showdown
    finish_before_showdown: List[str]  

class HandHistoryResponse(BaseModel):
    hands: List[Hand]