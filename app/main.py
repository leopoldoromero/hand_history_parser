import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router

app = FastAPI(
    title="Poker hand history parser",
    openapi_url=f"/api/v1/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)