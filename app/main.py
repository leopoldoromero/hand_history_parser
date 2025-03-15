from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.main import api_router
from contextlib import asynccontextmanager
from app.hand.application.generate_stats_after_hands_saved import (
    GenerateStatsAfterHandsSaved,
)
from app.shared.config.app_config import ALLOWED_HOSTS, APPLICATION_TITLE, OPENAPI_PATH
from app.shared.infrastructure.tasks.task_scheduler import task_scheduler
from app.shared.infrastructure.di_container import mongo_db_client
from mangum import Mangum


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

app.include_router(api_router, prefix="/api")

handler = Mangum(app)
