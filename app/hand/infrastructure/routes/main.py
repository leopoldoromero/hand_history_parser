from fastapi import APIRouter
from app.hand.infrastructure.routes import (
    get_hand_route,
    get_hands_route,
    upload_hands_route,
    get_stats_route,
    delete_hands_route,
)

router = APIRouter(prefix="/v1/hands", tags=["hands"])

router.include_router(get_hand_route.router)
router.include_router(get_hands_route.router)
router.include_router(upload_hands_route.router)
router.include_router(get_stats_route.router)
router.include_router(delete_hands_route.router)
