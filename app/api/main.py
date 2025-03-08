from fastapi import APIRouter
from app.api.routes import calculate_equity
from app.api.routes import auth
from app.hand.infrastructure.routes import get_hand_route
from app.hand.infrastructure.routes import get_hands_route
from app.hand.infrastructure.routes import upload_hands_route
from app.hand.infrastructure.routes import get_stats_route
from app.hand.infrastructure.routes import delete_hands_route
from app.auth.infrastructure.routes import login_route
from app.user.infrastructure.routes import create_user_route

api_router = APIRouter()

api_router.include_router(calculate_equity.router)
api_router.include_router(auth.router)

# Hands routes
api_router.include_router(get_hand_route.router)
api_router.include_router(get_hands_route.router)
api_router.include_router(upload_hands_route.router)
api_router.include_router(get_stats_route.router)
api_router.include_router(delete_hands_route.router)

# Auth routes
api_router.include_router(login_route.router)

# User routes
api_router.include_router(create_user_route.router)
