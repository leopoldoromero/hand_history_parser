from fastapi import APIRouter, HTTPException, Cookie, Depends
from typing import List
from app.hand.infrastructure.dtos.hand_response import HandResponseDto
from app.hand.domain.hand_repository import (
    HandRepository,
)
from app.shared.infrastructure.di_container import get_dependency


router = APIRouter(prefix="/v1", tags=["hands"])


@router.get(
    "/hands",
    response_model=List[HandResponseDto],
    summary="Get all hands for the user",
    description="Retrieves a list of all hands associated with the user, identified via the 'user_id' cookie.",
    responses={
        200: {"description": "List of hands successfully retrieved."},
        401: {"description": "User ID is missing from cookies."},
        500: {"description": "Internal server error."},
    },
)
async def run(
    user_id: str = Cookie(None),
    hands_repository: HandRepository = Depends(
        lambda: get_dependency("hands_repository")
    ),
):
    try:
        if not user_id:
            raise HTTPException(status_code=401, detail="Missing user_id in cookies")

        existing_hands = await hands_repository.get_all(user_id)
        print(f"Hands: {existing_hands}")
        return existing_hands

    except HTTPException as e:
        raise e

    except Exception as e:
        print(f"Unhandled error: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving hands: {str(e)}")
