from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from app.shared.infrastructure.di_container import get_dependency
from fastapi import status

router = APIRouter()


class CreateUserRequest(BaseModel):
    email: str
    password: str
    username: Optional[str] = None


@router.post("/")
async def run(
    body: CreateUserRequest,
    user_creator=Depends(lambda: get_dependency("user_creator")),
):
    await user_creator.execute(body.email, body.password, body.username)
    return JSONResponse(content={"success": True}, status_code=status.HTTP_201_CREATED)
