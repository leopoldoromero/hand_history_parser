from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.api.dtos.hand_history_response import HandHistoryResponse
from app.history_parser.history_parser import HistoryParser

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
        return JSONResponse({
            "filename": file.filename,
            "content_type": file.content_type,
            "content_preview": content_text[:100],
            "data": response[:2],
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
