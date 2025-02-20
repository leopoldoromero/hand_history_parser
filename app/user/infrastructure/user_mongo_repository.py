from app.shared.infrastructure.db import users_collection
from app.user.infrastructure.user_schema import UserSchema
from app.user.domain.user import UserRepository
from app.user.domain.user import User

class UserMongoRepository(UserRepository):
    """MongoDB implementation of UserRepository."""
    async def create(self, user: User) -> None:
        """Insert a new user into MongoDB."""
        await users_collection.insert_one(UserSchema.from_domain(user))

    async def get(self, user_id: str) -> User:
        """Retrieve a user by ID."""
        user = await users_collection.find_one({"id": user_id})
        if user:
            return User(id=user["id"], email=user["email"], password=user["password"])
        return None