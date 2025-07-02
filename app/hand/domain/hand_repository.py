from abc import ABC, abstractmethod
from app.hand.domain.hand import Hand
from typing import List, Optional, Tuple
from app.shared.domain.criteria import Criteria


class HandRepository(ABC):
    """Abstract repository for hand persistence."""

    @abstractmethod
    async def create(self, hand: Hand) -> None:
        """Create a new hand."""
        pass

    @abstractmethod
    async def get(self, hand_id: str) -> Hand:
        """Retrieve a hand by ID."""
        pass

    @abstractmethod
    async def get_all_by_user(self, user_id: str) -> List[Hand]:
        """Retrieve a hand by ID."""
        pass

    @abstractmethod
    async def get_all_by_criteria(self, criteria: Optional[Criteria]) -> List[Hand]:
        """Retrieve a hand by ID."""
        pass

    @abstractmethod
    async def get_with_neighbors(
        self, hand_id: str, user_id: str
    ) -> Tuple[Optional[Hand], Optional[str], Optional[str]]:
        """Retrieve a hand by ID."""
        pass

    @abstractmethod
    async def delete_all(self, user_id: str) -> None:
        """Delete all user hands by its ID."""
        pass
