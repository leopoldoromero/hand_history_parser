from typing import List
from app.shared.domain.criteria import Criteria
from app.user.infrastructure.persistance.mongo.user_schema import UserSchema
from app.user.domain.user_repository import UserRepository
from app.user.domain.user import User
from typing import Optional
from app.shared.infrastructure.persistance.mongo.criteria_to_mongo_query import (
    criteria_to_mongo_query,
)
from app.shared.infrastructure.persistance.mongo.db_client import DataBase

users_collection_name = "users"


class UserMongoRepository(UserRepository):
    """MongoDB implementation of UserRepository."""

    def __init__(self, conn: DataBase) -> None:
        self.conn = conn

    async def create(self, user: User) -> None:
        """Insert a new user into MongoDB."""
        await self.conn.get_collection(users_collection_name).insert_one(
            UserSchema.from_domain(user).model_dump()
        )

    async def get(self, user_id: str) -> Optional[User]:
        """Retrieve a user by ID."""
        user_data = await self.conn.get_collection(users_collection_name).find_one(
            {"id": user_id}
        )
        if user_data:
            user_entity = UserSchema(**user_data)
            return user_entity.to_domain()

        return None

    async def get_by_criteria(self, criteria: Criteria) -> List[User]:
        query, options = criteria_to_mongo_query(criteria)
        cursor = self.conn.get_collection(users_collection_name).find(query)
        if options["sort"]:
            cursor = cursor.sort(options["sort"])
        if options["skip"]:
            cursor = cursor.skip(options["skip"])
        if options["limit"]:
            cursor = cursor.limit(options["limit"])

        users = await cursor.to_list(length=None)
        return [UserSchema(**user).to_domain() for user in users]
