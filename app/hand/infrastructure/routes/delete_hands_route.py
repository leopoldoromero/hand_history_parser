from fastapi import APIRouter, HTTPException, Cookie, Depends
from app.hand.infrastructure.dtos.delete_hands_response import DeleteHandsResponseDto
from app.hand.domain.hand_repository import (
    HandRepository,
)
from app.shared.infrastructure.di_container import get_dependency

router = APIRouter(prefix="/v1", tags=["hands"])


@router.delete(
    "/hands",
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
    user_id: str = Cookie(None),
    hands_repository: HandRepository = Depends(
        lambda: get_dependency("hands_repository")
    ),
):
    try:
        if not user_id:
            raise HTTPException(status_code=401, detail="Missing user_id in cookies")

        await hands_repository.delete_all(user_id)

        return {"success": True}

    except HTTPException as e:
        raise e

    except Exception as e:
        print(f"Unhandled error: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving hand: {str(e)}")
