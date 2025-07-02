from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.hand.infrastructure.dtos.hand_response import HandResponseDto
from app.hand.domain.hand_repository import (
    HandRepository,
)
from app.shared.infrastructure.di_container import get_dependency
from app.shared.infrastructure.auth.get_optional_auth_user import get_optional_auth_user
from app.shared.infrastructure.auth.extract_guest_id import extract_guest_id

router = APIRouter()


@router.get(
    "/",
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
    guest_id: str = Depends(extract_guest_id),
    hands_repository: HandRepository = Depends(
        lambda: get_dependency("hands_repository")
    ),
    user=Depends(get_optional_auth_user),
):
    try:
        if not user and not guest_id:
            raise HTTPException(status_code=401, detail="Missing token and guest_id")
        user_id = user.id if user else guest_id
        existing_hands = await hands_repository.get_all_by_user(user_id)
        print(f"Hands: {existing_hands}")
        return existing_hands

    except HTTPException as e:
        raise e

    except Exception as e:
        print(f"Unhandled error: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving hands: {str(e)}")
