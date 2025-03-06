import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.main import api_router
from contextlib import asynccontextmanager
from app.hand.application.generate_stats_after_hands_saved import (
    GenerateStatsAfterHandsSaved,
)
from app.shared.config.app_config import ALLOWED_HOSTS, APPLICATION_TITLE, OPENAPI_PATH
from app.shared.infrastructure.persistance.mongo.db_client import mongoDbClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle management."""
    await mongoDbClient.connect_to_mongo()
    GenerateStatsAfterHandsSaved()  # ✅ Initialize here
    yield
    print("Shutting down...")
    await mongoDbClient.close_mongo_connection()


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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
