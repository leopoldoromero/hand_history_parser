from fastapi import Depends
from app.user.domain.exceptions.user_does_not_exist_exception import (
    UserDoesNotExistException,
)
from app.auth.domain.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.auth.infrastructure.jwt.jwt_handler import JwtHandler
from typing import Optional
from app.shared.infrastructure.crypto.crypto_utils import verify_password
from app.shared.domain.criteria import Criteria, CriteriaFilter, CriteriaOperators
from app.shared.infrastructure.di_container import get_dependency
from app.user.domain.user_repository import UserRepository


class Login:
    def __init__(
        self,
        token_handler: JwtHandler,
        users_repository: UserRepository = Depends(
            lambda: get_dependency("users_repository")
        ),
    ) -> None:
        self.token_handler = token_handler
        self.users_repository = users_repository

    async def execute(self, email: str, password: str) -> Optional[str]:
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
        user = user_or_null[0]
        if not user:
            raise UserDoesNotExistException()

        if not verify_password(password, user.password):
            raise InvalidCredentialsException()

        return self.token_handler.create_access_token(
            data={"sub": user.id},
        )


login = Login(JwtHandler())
