from fastapi import APIRouter
from app.user.infrastructure.routes import create_user_route, get_me_route

router = APIRouter(prefix="/v1/users", tags=["users"])

router.include_router(create_user_route.router)
router.include_router(get_me_route.router)
