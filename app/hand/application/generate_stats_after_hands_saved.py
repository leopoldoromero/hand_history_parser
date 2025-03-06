from app.shared.infrastructure.event_bus import event_bus
from app.hand.infrastructure.persistance.mongo.stats_mongo_repository import (
    stats_mongo_repository,
)
from app.hand.infrastructure.persistance.mongo.hand_mongo_repository import (
    hand_mongo_repository,
)
from app.hand.application.stats_generator import StatsGenerator


class GenerateStatsAfterHandsSaved:
    """A service that listens for hand updates and generates stats."""

    def __init__(self):
        print("Load...")
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
        hands = await hand_mongo_repository.get_all(user_id)

        stats_generator = StatsGenerator(hands)

        stats = stats_generator.execute()
        await stats_mongo_repository.persist(user_id, stats)
