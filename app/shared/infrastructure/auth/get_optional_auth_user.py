from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from app.auth.application.authenticator import Authenticator
from app.shared.infrastructure.di_container import get_dependency
from app.auth.domain.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


async def get_optional_auth_user(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
    authenticator: Authenticator = Depends(lambda: get_dependency("authenticator")),
):
    if not token:
        request.state.user = None
        return None

    try:
        user = await authenticator.authenticate_token(token)
        request.state.user = user
        return user
    except InvalidCredentialsException:
        request.state.user = None
        return None
