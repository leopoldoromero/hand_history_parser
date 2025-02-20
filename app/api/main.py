from fastapi import APIRouter

from app.api.routes import upload_history
from app.api.routes import calculate_equity
from app.api.routes import generate_stats_from_file
from app.api.routes import auth
from app.hand.infrastructure.routes import get_hand_route
from app.hand.infrastructure.routes import get_hands_route


api_router = APIRouter()
api_router.include_router(upload_history.router)
api_router.include_router(calculate_equity.router)
api_router.include_router(generate_stats_from_file.router)
api_router.include_router(auth.router)

# Hands routes
api_router.include_router(get_hand_route.router)
api_router.include_router(get_hands_route.router)

