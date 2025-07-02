from fastapi import APIRouter, HTTPException, Depends, Request
from app.hand.infrastructure.dtos.hand_response import GetHandResponseDto
from app.shared.infrastructure.di_container import get_dependency
from app.hand.domain.hand_repository import (
    HandRepository,
)
from app.shared.infrastructure.auth.get_optional_auth_user import get_optional_auth_user
from app.shared.infrastructure.auth.extract_guest_id import extract_guest_id

router = APIRouter()


@router.get(
    "/{hand_id}",
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
    request: Request,
    hand_id: str,
    guest_id: str = Depends(extract_guest_id),
    hands_repository: HandRepository = Depends(
        lambda: get_dependency("hands_repository")
    ),
    user=Depends(get_optional_auth_user),
):
    try:
        print(f"COOKIES: {request.cookies}")
        if not user and not guest_id:
            raise HTTPException(status_code=401, detail="Missing token and guest_id")

        user_id = user.id if user else guest_id
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
