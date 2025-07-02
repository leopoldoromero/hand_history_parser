from abc import ABC, abstractmethod
from app.hand.domain.stats import Stats


class StatsRepository(ABC):
    """Abstract repository for hand persistence."""

    @abstractmethod
    async def get_all(self, user_id: str) -> Stats:
        """Retrieve a hand by ID."""
        pass

    @abstractmethod
    async def persist(self, stats: Stats) -> None:
        """Create a new hand."""
        pass
