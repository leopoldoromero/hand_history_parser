from fastapi import APIRouter, HTTPException, Depends
from app.hand.infrastructure.dtos.generate_stats_response import GenerateStatsResponse
from app.shared.infrastructure.di_container import get_dependency
from app.hand.domain.stats_repository import (
    StatsRepository,
)
from app.shared.infrastructure.auth.get_optional_auth_user import get_optional_auth_user
from app.shared.infrastructure.auth.extract_guest_id import extract_guest_id

router = APIRouter()


@router.get(
    "/stats",
    response_model=GenerateStatsResponse,
    summary="Get a specific stats for user id",
    description="Retrieves a specific stats by user ID and includes.",
    responses={
        200: {"description": "stats successfully retrieved."},
        401: {"description": "User ID is missing from cookies."},
        404: {"description": "stats not found."},
        500: {"description": "Internal server error."},
    },
)
async def run(
    guest_id: str = Depends(extract_guest_id),
    stats_repository: StatsRepository = Depends(
        lambda: get_dependency("stats_repository")
    ),
    user=Depends(get_optional_auth_user),
):
    try:
        if not user and not guest_id:
            raise HTTPException(status_code=401, detail="Missing token and guest_id")

        user_id = user.id if user else guest_id

        stats = await stats_repository.get_all(user_id)

        if not stats:
            raise HTTPException(
                status_code=400, detail="There are no stats available yet"
            )

        return stats.players_stats

    except HTTPException as e:
        print(f"EXCEPTION {e}")
        raise e

    except Exception as e:
        print(f"Unhandled error: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")
