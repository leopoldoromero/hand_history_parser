from app.auth.domain.exceptions import (
    TokenExpiredException,
    InvalidTokenSignatureException,
    InvalidTokenException,
    DecodeTokenSignatureException,
)
from app.auth.infrastructure.jwt.jwt_handler import JwtHandler
from app.user.domain.user_repository import UserRepository
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
    DecodeError,
    InvalidTokenError,
)


class Authenticator:
    def __init__(
        self,
        token_handler: JwtHandler,
        user_repository: UserRepository,
    ) -> None:
        self.token_handler = token_handler
        self.user_repository = user_repository

    async def authenticate_token(self, token: str):
        try:
            user_id = self.token_handler.decode_token(token)
            return await self.user_repository.get(user_id)
        except ExpiredSignatureError:
            raise TokenExpiredException()
        except InvalidSignatureError:
            raise InvalidTokenSignatureException()
        except DecodeError:
            raise DecodeTokenSignatureException()
        except InvalidTokenError:
            raise InvalidTokenException()
