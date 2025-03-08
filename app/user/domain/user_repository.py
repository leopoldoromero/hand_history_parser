from abc import ABC, abstractmethod
from app.user.domain.user import User
from typing import List, Optional
from app.shared.domain.criteria import Criteria


class UserRepository(ABC):
    """Abstract repository for user persistence."""

    @abstractmethod
    async def create(self, user: User) -> None:
        """Create a new user."""
        pass

    @abstractmethod
    async def get(self, user_id: str) -> Optional[User]:
        """Retrieve a user by ID."""
        pass

    @abstractmethod
    async def get_by_criteria(self, criteria: Criteria) -> List[User]:
        """Retrieve a user by ID."""
        pass
