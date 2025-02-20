from fastapi import APIRouter, File, UploadFile, HTTPException, Cookie
from fastapi.responses import JSONResponse
from app.api.dtos.hand_history_response import HandHistoryResponse
from app.history_parser.history_parser import HistoryParser
from app.stats_generator.stats_generator import StatsGenerator
# import json
from datetime import datetime
from app.hand.domain.hand_repository import HandRepository
from app.hand.infrastructure.persistance.hand_json_repository import HandJsonRepository
from app.hand.domain.hand import Hand, GeneralInfo, Player, Action, Summary

router = APIRouter(prefix="/v1", tags=["history"])
hand_repository = HandJsonRepository()

@router.post("/history", response_model=HandHistoryResponse)
async def run(file: UploadFile = File(...), user_id: str = Cookie(None)):
    try:
        AVAILABLE_FILE_FORMATS = ["text/plain"]

        if file.content_type not in AVAILABLE_FILE_FORMATS:
            raise HTTPException(status_code=400, detail=f"Invalid file type. The allowed formats are: {', '.join(AVAILABLE_FILE_FORMATS)}")

        content = await file.read()
        content_text = content.decode("utf-8")  
        parser = HistoryParser(content_text)
        response = parser.parse()
        for hand in response:
            hand_instance = Hand.from_primitives({
                "id": hand["id"],
                "user_id": user_id,
                "general_info":hand["general_info"],  # Unpacking dictionary into dataclass
                "table_name":hand["table_name"],
                "table_type":hand["table_type"],
                "button_seat":hand["button_seat"],
                "players":hand["players"],  # Convert list of dicts to list of Player objects
                "hero_cards":hand["hero_cards"],
                "hero_name":hand["hero_name"],
                "hero_seat":hand["hero_seat"],
                "actions":hand["actions"],  # Convert list of dicts to list of Action objects
                "summary": hand["summary"]
            })
            await hand_repository.create(hand_instance)

        return JSONResponse({"data": response})
    
    except HTTPException as e:
        raise e  # Rethrow expected exceptions properly
    
    except Exception as e:
        print(f"Unhandled error: {e}")  # Debugging output
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")