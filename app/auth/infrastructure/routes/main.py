from fastapi import APIRouter
from app.auth.infrastructure.routes import login_route, refresh_route

router = APIRouter(prefix="/v1/auth", tags=["auth"])

router.include_router(login_route.router)
router.include_router(refresh_route.router)
