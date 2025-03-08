from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.application.login import login
from app.auth.infrastructure.dtos.login_request import LoginRequest
from app.auth.domain.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.user.domain.exceptions.user_does_not_exist_exception import (
    UserDoesNotExistException,
)
from app.auth.application.authenticator import authenticator
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/login")
async def login_for_access_token(login_data: LoginRequest):
    try:
        access_token = await login.execute(login_data.email, login_data.password)
        return {"access_token": access_token}
    except InvalidCredentialsException as e:
        print(f"Exception 1: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserDoesNotExistException as e:
        print(f"Exception 2: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.detail,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Protected route
@router.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        user = authenticator.authentica_token(token)
        print(f"User: {user}")
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=401, detail=e.detail)
