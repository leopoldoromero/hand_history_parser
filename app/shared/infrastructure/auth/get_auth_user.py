from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.auth.application.authenticator import Authenticator
from app.shared.infrastructure.di_container import get_dependency
from app.shared.domain import BaseAppException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


async def get_auth_user(
    token: str = Depends(oauth2_scheme),
    authenticator: Authenticator = Depends(lambda: get_dependency("authenticator")),
):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token"
        )

    try:
        user = await authenticator.authenticate_token(token)
    except BaseAppException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=e.to_dict()
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    return user
