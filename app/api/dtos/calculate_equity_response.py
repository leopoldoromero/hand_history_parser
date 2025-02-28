from pydantic import BaseModel

class CalculateHandVsRangeEquityResponse(BaseModel):
    hand_equity: float
    range_equity: float
    tie_equity: float
