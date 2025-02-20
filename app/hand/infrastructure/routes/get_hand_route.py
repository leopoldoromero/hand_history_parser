from fastapi import APIRouter, HTTPException, Cookie, Request
from app.hand.infrastructure.persistance.hand_json_repository import HandJsonRepository
from app.hand.infrastructure.dtos.hand_response import GetHandResponseDto

router = APIRouter(prefix="/v1", tags=["hands"])
hand_repository = HandJsonRepository()

DEFAULT_USER_ID = "75565b68-ed1f-11ef-901b-0ade7a4f7cd3"

@router.get("/hands/{hand_id}",
            response_model=GetHandResponseDto,
            summary="Get a specific hand by ID",
            description="Retrieves a specific hand by its ID and includes navigation details for the previous and next hands.",
            responses={
                 200: { "description": "Hand successfully retrieved." },
                401: {"description": "User ID is missing from cookies."},
                404: {"description": "Hand not found."},
                500: {"description": "Internal server error."},
            }
    )
async def run(request: Request, hand_id: str, user_id: str = Cookie(None)):
    """Retrieve a specific hand by its ID and provide next/previous navigation."""
    try:
        if not user_id:
            raise HTTPException(status_code=401, detail="Missing user_id in cookies")

        hand, prev_hand_id, next_hand_id = await hand_repository.get_with_neighbors(hand_id, user_id)
        
        if not hand:
            raise HTTPException(status_code=404, detail="Hand not found")

        return {
            "hand": hand,
            "prev_hand_id": prev_hand_id,
            "next_hand_id": next_hand_id
        }
    
    except HTTPException as e:
        raise e  
    
    except Exception as e:
        print(f"Unhandled error: {e}")  
        raise HTTPException(status_code=500, detail=f"Error retrieving hand: {str(e)}")
