from fastapi import APIRouter, HTTPException, Cookie
from app.hand.infrastructure.persistance.hand_json_repository import hand_repository
from typing import List
from app.hand.infrastructure.dtos.hand_response import HandResponseDto

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
async def run(user_id: str = Cookie(None)):
    """Retrieve all hands for the user."""
    try:
        if not user_id:
            raise HTTPException(status_code=401, detail="Missing user_id in cookies")

        existing_hands = await hand_repository.get_all(user_id)
        return existing_hands

    except HTTPException as e:
        raise e

    except Exception as e:
        print(f"Unhandled error: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving hands: {str(e)}")
