from fastapi import APIRouter, HTTPException, Cookie
from app.hand.infrastructure.persistance.mongo.stats_mongo_repository import (
    stats_mongo_repository,
)
from app.hand.infrastructure.dtos.generate_stats_response import GenerateStatsResponse

router = APIRouter(prefix="/v1", tags=["stats"])


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
async def run(user_id: str = Cookie(None)):
    try:
        if not user_id:
            raise HTTPException(status_code=401, detail="Missing user_id in cookies")

        stats = await stats_mongo_repository.get_all(user_id)

        if not stats:
            raise HTTPException(
                status_code=400, detail="There are no stats available yet"
            )

        return stats.stats

    except HTTPException as e:
        raise e

    except Exception as e:
        print(f"Unhandled error: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")
