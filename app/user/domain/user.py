import uuid
from typing import Optional
from app.user.domain.exceptions import (
    InvalidEmailException,
    InvalidPasswordException,
)


class User:
    MIN_PASSWORD_LENGTH = 6

    def __init__(self, id: str, email: str, password: str, username: str) -> None:
        self.id = id if id else str(uuid.uuid4())
        self.email = email
        self.password = password
        self.username = username

    @staticmethod
    def create(email: str, password: str, username: Optional[str]) -> "User":
        User.validate(email, password)
        if not username:
            username = email.split("@")[0]
        return User(
            id=str(uuid.uuid4()), email=email, password=password, username=username
        )

    @staticmethod
    def validate(email: str, password: str) -> None:
        if not email or "@" not in email:
            raise InvalidEmailException()
        if not password or len(password) < User.MIN_PASSWORD_LENGTH:
            raise InvalidPasswordException()
        # if not username:
        #     raise ValueError("Username cannot be empty")
