from app.user.domain.exceptions.user_does_not_exist_exception import (
    UserDoesNotExistException,
)
from app.auth.domain.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.auth.infrastructure.jwt.jwt_handler import JwtHandler
from typing import Optional
from app.shared.infrastructure.crypto.crypto_utils import verify_password


class Authenticator:
    def __init__(self, token_handler: JwtHandler) -> None:
        self.token_handler = token_handler
        self.fake_users_db = {
            "user1@example.com": {
                "id": "75565b68-ed1f-11ef-901b-0ade7a4f7cd3",
                "username": "user1",
                "full_name": "John Doe",
                "email": "user1@example.com",
                "hashed_password": "$2b$12$IU5OvHGBRT7vEfO/j5b9Z.7f5Pao8u.xhsxvWXcF5R4jeqcdAS4/m",
            }
        }

    def authenticate(self, email: str, password: str) -> Optional[str]:
        user = self.fake_users_db.get(email)
        if not user:
            raise UserDoesNotExistException()

        if not verify_password(password, user["hashed_password"]):
            raise InvalidCredentialsException()

        return self.token_handler.create_access_token(
            data={"sub": user["id"]},
        )

    def authentica_token(self, token: str):
        user_id = self.token_handler.decode_token(token)
        user = self.fake_users_db.get("user1@example.com")
        if not user:
            raise UserDoesNotExistException()
        if user["id"] != user_id:
            raise InvalidCredentialsException()
        return user


authenticator = Authenticator(JwtHandler())
