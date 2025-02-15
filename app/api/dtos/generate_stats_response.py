from pydantic import BaseModel
from typing import Dict

class PlayerStatsResponse(BaseModel):
    HANDS: int
    FOLD: int 
    LIMP: int
    OR: int
    ROL: int 
    THREE_BET: int
    SQUEEZE: int
    FOUT_BET: int
    CALL_TO_OR: int
    CALL_TO_ROL : int
    CALL_TO_3BET: int
    CALL_TO_SQUEEZE: int
    CALL_TO_4BET: int
    FOLD_TO_3BET: int
    FOLD_TO_SQUEEZE: int
    FOLD_TO_4BET: int
    THREE_BET_OPP: int

GenerateStatsResponse = Dict[str, PlayerStatsResponse]
