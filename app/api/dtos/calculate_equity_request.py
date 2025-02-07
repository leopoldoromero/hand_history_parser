from pydantic import BaseModel

class CalculateHandVsRangeEquityRequest(BaseModel):
    hand: list
    range: list 
    board: list = []