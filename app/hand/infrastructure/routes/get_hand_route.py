from fastapi import APIRouter, HTTPException, Cookie, Depends
from app.hand.infrastructure.dtos.hand_response import GetHandResponseDto
from app.shared.infrastructure.di_container import get_dependency
from app.hand.domain.hand_repository import (
    HandRepository,
)

router = APIRouter(prefix="/v1", tags=["hands"])


@router.get(
    "/hands/{hand_id}",
    response_model=GetHandResponseDto,
    summary="Get a specific hand by ID",
    description="Retrieves a specific hand by its ID and includes navigation details for the previous and next hands.",
    responses={
        200: {"description": "Hand successfully retrieved."},
        401: {"description": "User ID is missing from cookies."},
        404: {"description": "Hand not found."},
        500: {"description": "Internal server error."},
    },
)
async def run(
    hand_id: str,
    user_id: str = Cookie(None),
    hands_repository: HandRepository = Depends(
        lambda: get_dependency("hands_repository")
    ),
):
    try:
        if not user_id:
            raise HTTPException(status_code=401, detail="Missing user_id in cookies")

        (
            hand,
            prev_hand_id,
            next_hand_id,
        ) = await hands_repository.get_with_neighbors(hand_id, user_id)

        if not hand:
            raise HTTPException(status_code=404, detail="Hand not found")

        return {
            "hand": hand,
            "prev_hand_id": prev_hand_id,
            "next_hand_id": next_hand_id,
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        print(f"Unhandled error: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving hand: {str(e)}")
