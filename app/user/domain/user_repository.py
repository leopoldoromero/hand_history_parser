from abc import ABC, abstractmethod
from app.user.domain.user import User

class UserRepository(ABC):
    """Abstract repository for user persistence."""

    @abstractmethod
    async def create(self, user: User) -> None:
        """Create a new user."""
        pass

    @abstractmethod
    async def get(self, user_id: str) -> User:
        """Retrieve a user by ID."""
        pass
