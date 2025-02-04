from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.api.dtos.hand_history_response import HandHistoryResponse
from app.history_parser.history_parser import HistoryParser
from app.stats_generator.stats_generator import StatsGenerator
import json

router = APIRouter(prefix="/v1", tags=["upload"])

@router.post("/upload", response_model=HandHistoryResponse)
async def run(file: UploadFile = File(...)):
    try:
        AVAILABLE_FILE_FORMATS = ["text/plain"]

        if file.content_type not in AVAILABLE_FILE_FORMATS:
             raise HTTPException(status_code=400, detail=f"Invalid file type. The allowed formats are: {', '.join(AVAILABLE_FILE_FORMATS)}")

        content = await file.read()
        
        content_text = content.decode("utf-8")  
        parser = HistoryParser(content_text)
        response = parser.parse()
        # TODO: this part would be in other route, this is only for testing. 

        stats_generator = StatsGenerator(response)
        data = stats_generator.execute()


        file_path = "player_stats.json"

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
                

        return JSONResponse({
            "filename": file.filename,
            "content_type": file.content_type,
            "content_preview": content_text[:10000],
            "data": response[58:60],
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
