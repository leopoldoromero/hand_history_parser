from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.api.dtos.calculate_equity_response import CalculateHandVsRangeEquityResponse
from app.api.dtos.calculate_equity_request import CalculateHandVsRangeEquityRequest
from app.equity_calculator.hand_vs_range_calculator import HandVsRangeEquityCalculator

router = APIRouter(prefix="/v1", tags=["calculate"])

@router.post("/calculate/equity", response_model=CalculateHandVsRangeEquityResponse)
async def run(
    request: CalculateHandVsRangeEquityRequest = None,
):
    try:
        calculator = HandVsRangeEquityCalculator()

        hand_equity, range_equity, tie_equity = calculator.execute(request.hand, request.range, request.board)

        return JSONResponse({
            "hand_equity": hand_equity,
            "range_equity": range_equity,
            "tie_equity": tie_equity,
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating the equity of the hand: {str(e)}")
