from fastapi import APIRouter

from app.api.routes import upload_history
from app.api.routes import calculate_equity
from app.api.routes import generate_stats_from_file

api_router = APIRouter()
api_router.include_router(upload_history.router)
api_router.include_router(calculate_equity.router)
api_router.include_router(generate_stats_from_file.router)

