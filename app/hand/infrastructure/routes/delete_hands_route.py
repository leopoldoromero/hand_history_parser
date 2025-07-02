from fastapi import APIRouter, HTTPException, Depends
from app.hand.infrastructure.dtos.delete_hands_response import DeleteHandsResponseDto
from app.hand.domain.hand_repository import (
    HandRepository,
)
from app.shared.infrastructure.di_container import get_dependency
from app.shared.infrastructure.auth.extract_guest_id import extract_guest_id

router = APIRouter()


@router.delete(
    "/",
    response_model=DeleteHandsResponseDto,
    summary="Delete user hands",
    description="Delete all the hands uploaded by the user.",
    responses={
        200: {"description": "Hands successfully deleted."},
        401: {"description": "User ID is missing from cookies."},
        500: {"description": "Internal server error."},
    },
)
async def run(
    guest_id: str = Depends(extract_guest_id),
    hands_repository: HandRepository = Depends(
        lambda: get_dependency("hands_repository")
    ),
):
    try:
        if not guest_id:
            raise HTTPException(status_code=401, detail="Missing guest_id in cookies")

        await hands_repository.delete_all(guest_id)

        return {"success": True}

    except HTTPException as e:
        raise e

    except Exception as e:
        print(f"Unhandled error: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving hand: {str(e)}")
