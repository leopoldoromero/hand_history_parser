from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from app.shared.infrastructure.di_container import get_dependency
from app.shared.infrastructure.auth.get_auth_user import get_auth_user
from app.auth.infrastructure.jwt.jwt_handler import JwtHandler
from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


@router.get("/refresh", response_model=RefreshTokenResponse)
async def run(
    user=Depends(get_auth_user),
    token_handler: JwtHandler = Depends(lambda: get_dependency("token_handler")),
):
    access_token, refresh_token = token_handler.create_access_and_refresh_tokens(
        data={"sub": user.id},
    )
    res = JSONResponse(
        content={"access_token": access_token, "refresh_token": refresh_token}
    )
    return res
