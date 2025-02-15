from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.api.dtos.generate_stats_response import GenerateStatsResponse
from app.history_parser.history_parser import HistoryParser
from app.stats_generator.stats_generator import StatsGenerator
# import json
from datetime import datetime


router = APIRouter(prefix="/v1", tags=["stats"])

@router.post("/stats", response_model=GenerateStatsResponse)
async def run(file: UploadFile = File(...)):
    try:
        AVAILABLE_FILE_FORMATS = ["text/plain"]

        if file.content_type not in AVAILABLE_FILE_FORMATS:
             raise HTTPException(status_code=400, detail=f"Invalid file type. The allowed formats are: {', '.join(AVAILABLE_FILE_FORMATS)}")

        content = await file.read()
        
        content_text = content.decode("utf-8")  
        parser = HistoryParser(content_text)
        response = parser.parse()

        stats_generator = StatsGenerator(response)
        data = stats_generator.execute()


        #timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # file_path = f"player_stats_{timestamp}.json"

        # with open(file_path, 'w') as json_file:
        #     json.dump(data, json_file, indent=4)
                

        return JSONResponse({
            # "filename": file.filename,
            # "content_type": file.content_type,
            # "content_preview": content_text[:10000],
            "data": data,
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
