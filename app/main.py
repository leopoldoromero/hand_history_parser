from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.hand.application.generate_stats_after_hands_saved import (
    GenerateStatsAfterHandsSaved,
)
from app.shared.config.app_config import ALLOWED_HOSTS, APPLICATION_TITLE, OPENAPI_PATH
from app.shared.domain.base_exception import BaseAppException
from app.shared.infrastructure.http.app_exception_handler import (
    base_app_exception_handler,
)
from app.shared.infrastructure.tasks.task_scheduler import task_scheduler
from app.shared.infrastructure.di_container import mongo_db_client
from mangum import Mangum
from app.auth.infrastructure.routes.main import router as auth_router
from app.user.infrastructure.routes.main import router as user_router
from app.hand.infrastructure.routes.main import router as hand_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle management."""
    if not task_scheduler.running:
        task_scheduler.start()
    await mongo_db_client.connect_to_mongo()
    GenerateStatsAfterHandsSaved()  # ✅ Initialize here
    yield
    print("Shutting down...")
    await mongo_db_client.close_mongo_connection()


app = FastAPI(
    title=APPLICATION_TITLE,
    openapi_url=OPENAPI_PATH,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(hand_router)

app.include_router(api_router, prefix="/api")

app.add_exception_handler(BaseAppException, base_app_exception_handler)

handler = Mangum(app)
