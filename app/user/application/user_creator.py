from fastapi import Depends
from app.user.domain.user import User
from app.shared.infrastructure.crypto.crypto_utils import hash_password
from app.shared.domain.criteria import Criteria, CriteriaFilter, CriteriaOperators
from app.user.domain.exceptions.user_already_exist_exception import (
    UserAlreadyExistException,
)
from app.user.domain.user_repository import UserRepository
from app.shared.infrastructure.di_container import get_dependency


class UserCreator:
    def __init__(
        self,
        users_repository: UserRepository = Depends(
            lambda: get_dependency("users_repository")
        ),
    ) -> None:
        self.users_repository = users_repository

    async def execute(self, email: str, password: str):
        user_or_null = await self.users_repository.get_by_criteria(
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
        user = User.create(email=email, password=hashed_password)
        await self.users_repository.create(user)


user_creator = UserCreator()
