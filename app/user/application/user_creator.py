from app.user.domain.user import User
from app.shared.infrastructure.crypto.crypto_utils import hash_password
from app.shared.domain.criteria import Criteria, CriteriaFilter, CriteriaOperators
from app.user.domain.exceptions import (
    UserAlreadyExistException,
)
from app.user.domain.user_repository import UserRepository
from typing import Optional


class UserCreator:
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    async def execute(self, email: str, password: str, username: Optional[str] = None):
        user_or_null = await self.user_repository.get_by_criteria(
            criteria=Criteria(
                filters=[
                    CriteriaFilter(
                        field="email", value=email, operator=CriteriaOperators.EQUAL
                    )
                ],
                page=1,
                limit=1,
            )
        )
        if len(user_or_null):
            raise UserAlreadyExistException()

        hashed_password = hash_password(password)
        user = User.create(email=email, password=hashed_password, username=username)
        await self.user_repository.create(user)
