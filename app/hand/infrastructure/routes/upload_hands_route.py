from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.hand.infrastructure.dtos.upload_hands_response import UploadHandsResponseDto
from app.history_parser.history_parser import HistoryParser
from app.hand.domain.hand import Hand
from app.shared.infrastructure.event_bus import event_bus
from app.hand.domain.hand_repository import (
    HandRepository,
)
from app.shared.infrastructure.di_container import get_dependency
from app.shared.infrastructure.auth.get_optional_auth_user import get_optional_auth_user
from app.shared.infrastructure.auth.extract_guest_id import extract_guest_id

router = APIRouter()


@router.post("/", response_model=UploadHandsResponseDto)
async def run(
    file: UploadFile = File(...),
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

        AVAILABLE_FILE_FORMATS = ["text/plain"]

        if file.content_type not in AVAILABLE_FILE_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. The allowed formats are: {', '.join(AVAILABLE_FILE_FORMATS)}",
            )

        content = await file.read()
        content_text = content.decode("utf-8")
        parser = HistoryParser(content_text)
        response = parser.parse()

        for hand in response:
            hand_instance = Hand.from_primitives(
                {
                    "id": hand["id"],
                    "user_id": user_id,
                    "general_info": hand["general_info"],
                    "table_name": hand["table_name"],
                    "table_type": hand["table_type"],
                    "button_seat": hand["button_seat"],
                    "players": hand["players"],
                    "hero_cards": hand["hero_cards"],
                    "hero_name": hand["hero_name"],
                    "hero_seat": hand["hero_seat"],
                    "actions": hand["actions"],
                    "summary": hand["summary"],
                }
            )
            await hands_repository.create(hand_instance)

        await event_bus.publish("hands_saved", {"user_id": user_id})

        return JSONResponse({"success": True})

    except HTTPException as e:
        raise e

    except Exception as e:
        print(f"Unhandled error: {e}")
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
