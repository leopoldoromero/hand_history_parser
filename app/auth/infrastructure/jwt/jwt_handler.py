import jwt
from datetime import datetime, timedelta
from app.shared.config.app_config import (
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ACCESS_TOKEN_EXPIRE_DAYS,
    JWT_SECRET_KEY,
)
from app.auth.domain.exceptions import (
    InvalidTokenException,
)


class JwtHandler:
    def create_access_and_refresh_tokens(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, str(JWT_SECRET_KEY), algorithm=str(JWT_ALGORITHM))
        expire = datetime.now() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        refresh_token = jwt.encode(
            to_encode, str(JWT_SECRET_KEY), algorithm=str(JWT_ALGORITHM)
        )
        return token, refresh_token

    def decode_token(self, token: str):
        payload = jwt.decode(
            token, str(JWT_SECRET_KEY), algorithms=[str(JWT_ALGORITHM)]
        )
        sub = payload.get("sub")
        if sub is None:
            raise InvalidTokenException()
        return sub
