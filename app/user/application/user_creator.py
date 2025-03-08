from app.user.infrastructure.persistance.mongo.user_mongo_repository import (
    users_mongo_repository,
)
from app.user.domain.user import User
from app.shared.infrastructure.crypto.crypto_utils import hash_password
from app.shared.domain.criteria import Criteria, CriteriaFilter, CriteriaOperators
from app.user.domain.exceptions.user_already_exist_exception import (
    UserAlreadyExistException,
)


class UserCreator:
    async def execute(self, email: str, password: str):
        user_or_null = await users_mongo_repository.get_by_criteria(
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
        await users_mongo_repository.create(user)


user_creator = UserCreator()
