from fastapi import Depends
from app.shared.infrastructure.event_bus import event_bus
from app.shared.infrastructure.di_container import get_dependency
from app.hand.domain.hand_repository import (
    HandRepository,
)
from app.hand.domain.stats_repository import (
    StatsRepository,
)
from app.hand.application.stats_generator import StatsGenerator


class GenerateStatsAfterHandsSaved:
    """A service that listens for hand updates and generates stats."""

    def __init__(
        self,
        hands_repository: HandRepository = Depends(
            lambda: get_dependency("hands_repository")
        ),
        stats_repository: StatsRepository = Depends(
            lambda: get_dependency("stats_repository")
        ),
    ):
        print("Load...")
        self.hands_repository = hands_repository
        self.stats_repository = stats_repository
        event_bus.subscribe("hands_saved", self.handle_hand_saved)

    async def handle_hand_saved(self, data: dict):
        """Callback to generate stats when a new hand is saved."""
        user_id = data["user_id"]
        print(f"📊 Generating stats for (user: {user_id})...")
        await self.generate_stats(user_id)
        """
        await stats_repository.persist(user_id)
        """

    async def generate_stats(self, user_id: str):
        """Simulated stats generation process."""
        # await asyncio.sleep(1)  # Simulate processing delay
        hands = await self.hands_repository.get_all(user_id)

        stats_generator = StatsGenerator(hands)

        stats = stats_generator.execute(user_id)
        await self.stats_repository.persist(user_id, stats)
