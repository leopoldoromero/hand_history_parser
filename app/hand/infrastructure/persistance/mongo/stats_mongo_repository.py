from typing import Optional
from app.hand.domain.stats import Stats
from app.hand.domain.stats_repository import StatsRepository
from app.hand.infrastructure.persistance.mongo.stats_schema import StatsSchema
from app.shared.infrastructure.persistance.mongo.db_client import DataBase

stats_collection_name = "stats"


class StatsMongoRepository(StatsRepository):
    """MongoDB-based repository for Stats."""

    def __init__(self, conn: DataBase) -> None:
        self.conn = conn

    # TODO: check lateer to remove user_id because is already included in the stats class
    async def persist(self, stats: Stats) -> None:
        """Save or update stats for a given user in MongoDB."""
        stats_schema = StatsSchema.from_domain(stats)
        existing_stats = await self.conn.get_collection(stats_collection_name).find_one(
            {"user_id": stats.user_id}
        )

        if existing_stats:
            await self.conn.get_collection(stats_collection_name).update_one(
                {"user_id": stats.user_id},
                {"$set": stats_schema.model_dump()},
            )
        else:
            await self.conn.get_collection(stats_collection_name).insert_one(
                stats_schema.model_dump()
            )

    async def get_all(self, user_id: str) -> Optional[Stats]:
        """Retrieve stats for a given user from MongoDB."""
        stats_data = await self.conn.get_collection(stats_collection_name).find_one(
            {"user_id": user_id}
        )
        # stats_data = await mongoDbClient.get_collection(stats_collection_name).find_one(
        #     {"user_id": user_id}
        # )
        if stats_data:
            return StatsSchema(**stats_data).to_domain()
        return None
