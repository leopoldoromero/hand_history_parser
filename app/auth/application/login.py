from app.auth.domain.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.auth.infrastructure.jwt.jwt_handler import JwtHandler
from typing import Tuple
from app.shared.infrastructure.crypto.crypto_utils import verify_password
from app.shared.domain.criteria import Criteria, CriteriaFilter, CriteriaOperators
from app.user.domain.user_repository import UserRepository


class Login:
    def __init__(
        self,
        token_handler: JwtHandler,
        user_repository: UserRepository,
    ) -> None:
        self.token_handler = token_handler
        self.user_repository = user_repository

    async def execute(self, email: str, password: str) -> Tuple[str, str]:
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
        user = user_or_null[0] if user_or_null else None
        if not user or not verify_password(password, user.password):
            raise InvalidCredentialsException()

        return self.token_handler.create_access_and_refresh_tokens(
            data={"sub": user.id},
        )
