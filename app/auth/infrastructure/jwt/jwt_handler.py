import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from app.shared.config.app_config import (
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
)
from app.auth.domain.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)


class JwtHandler:
    def create_access_token(
        self, data: dict, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    ):
        to_encode = data.copy()
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})
        try:
            return jwt.encode(
                to_encode, str(JWT_SECRET_KEY), algorithm=str(JWT_ALGORITHM)
            )
        except Exception as e:
            raise e

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(
                token, str(JWT_SECRET_KEY), algorithms=[str(JWT_ALGORITHM)]
            )
            sub = payload.get("sub")
            if sub is None:
                raise InvalidCredentialsException()
            return sub
        except InvalidTokenError:
            raise InvalidCredentialsException()
