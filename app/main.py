import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from app.api.main import api_router

app = FastAPI(
    title="Poker hand history parser",
    openapi_url=f"/api/v1/openapi.json",
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