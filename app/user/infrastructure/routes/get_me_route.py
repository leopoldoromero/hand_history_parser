from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from app.shared.infrastructure.auth.get_auth_user import get_auth_user
from pydantic import BaseModel
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


class GetMeUserResponse(BaseModel):
    id: str
    email: str
    username: str


@router.get("/me", response_model=Optional[GetMeUserResponse])
async def run(
    user=Depends(get_auth_user),
):
    return JSONResponse(
        content={
            "id": user.id,
            "email": user.email,
            "username": user.username,
        }
        if user is not None
        else None,
        status_code=status.HTTP_200_OK,
    )
