from fastapi import APIRouter, HTTPException, Cookie
from app.hand.infrastructure.hand_json_repository import HandJsonRepository
from typing import List, Optional
from app.hand.domain.hand import Hand
from pydantic import BaseModel
from app.api.dtos.hand_history_response import HandResponseDto, GetHandResponseDto

router = APIRouter(prefix="/v1", tags=["hands"])
hand_repository = HandJsonRepository()

@router.get("/hands", 
            response_model=List[HandResponseDto],
            summary="Get all hands for the user",
            description="Retrieves a list of all hands associated with the user, identified via the 'user_id' cookie.",
            responses={
                200: {"description": "List of hands successfully retrieved."},
                401: {"description": "User ID is missing from cookies."},
                500: {"description": "Internal server error."},
            },
        )
async def get_hands(user_id: str = Cookie(None)):
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
async def get_hand(hand_id: str, user_id: str = Cookie(None)):
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
