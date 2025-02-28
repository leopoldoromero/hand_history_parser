import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.main import api_router
from contextlib import asynccontextmanager
from app.hand.application.generate_stats_after_hands_saved import (
    GenerateStatsAfterHandsSaved,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle management."""
    GenerateStatsAfterHandsSaved()  # ✅ Initialize here
    yield  # Run the app
    print("Shutting down...")


app = FastAPI(
    title="Poker hand history parser",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan,
)

DEFAULT_USER_ID = "75565b68-ed1f-11ef-901b-0ade7a4f7cd3"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ✅ Must include "http://"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
