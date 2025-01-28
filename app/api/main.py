from fastapi import APIRouter

from app.api.routes import upload_history

api_router = APIRouter()
api_router.include_router(upload_history.router)

