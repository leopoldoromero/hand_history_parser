from app.hand.infrastructure.persistance.mongo.hand_schema import HandSchema
from app.hand.domain.hand_repository import HandRepository
from app.hand.domain.hand import Hand
from typing import Optional, Tuple, List
from app.shared.infrastructure.persistance.mongo.db_client import DataBase
from app.shared.domain.criteria import Criteria
from app.shared.infrastructure.persistance.mongo.criteria_to_mongo_query import (
    criteria_to_mongo_query,
)

hands_collection_name = "hands"


class HandMongoRepository(HandRepository):
    """MongoDB implementation of UserRepository."""

    def __init__(self, conn: DataBase) -> None:
        self.conn = conn

    async def create(self, hand: Hand) -> None:
        """Insert a new hand into MongoDB."""
        hand_exist = await self.conn.get_collection(hands_collection_name).find_one(
            {
                "general_info.room_hand_id": hand.general_info.room_hand_id,
                "user_id": hand.user_id,
            }
        )
        if not hand_exist:
            print(f"HAND SAVED: {hand.id}, USER: {hand.user_id}")
            await self.conn.get_collection(hands_collection_name).insert_one(
                HandSchema.from_domain(hand).model_dump()
            )
        else:
            print(f"HAND ALREADY EXIST: {hand.id}, USER: {hand.user_id}")

    async def get(self, hand_id: str) -> Optional[Hand]:
        """Retrieve a hand by ID."""
        hand_data = await self.conn.get_collection(hands_collection_name).find_one(
            {"id": hand_id}
        )
        if hand_data:
            hand_entiy = HandSchema(**hand_data)
            return hand_entiy.to_domain()

        return None

    async def get_all_by_user(self, user_id: str) -> list[Hand]:
        """Retrieve all hands belonging to a specific user."""
        hands_cursor = self.conn.get_collection(hands_collection_name).find(
            {"user_id": user_id}
        )
        hands_list = await hands_cursor.to_list(length=None)
        return [HandSchema(**hand).to_domain() for hand in hands_list]

    async def get_all_by_criteria(self, criteria: Optional[Criteria]) -> List[Hand]:
        if criteria is None:
            cursor = self.conn.get_collection(hands_collection_name).find({})
            hands = await cursor.to_list(length=None)
            return [HandSchema(**hand).to_domain() for hand in hands]

        query, options = criteria_to_mongo_query(criteria)
        cursor = self.conn.get_collection(hands_collection_name).find(query)
        if options["sort"]:
            cursor = cursor.sort(options["sort"])
        if options["skip"]:
            cursor = cursor.skip(options["skip"])
        if options["limit"]:
            cursor = cursor.limit(options["limit"])

        hands = await cursor.to_list(length=None)
        return [HandSchema(**hand).to_domain() for hand in hands]

    async def get_with_neighbors(
        self, hand_id: str, user_id: str
    ) -> Tuple[Optional[Hand], Optional[str], Optional[str]]:
        """Retrieve a hand along with its previous and next hand IDs."""
        collection = self.conn.get_collection(hands_collection_name)

        # Get the target hand
        hand_data = await collection.find_one({"id": hand_id, "user_id": user_id})
        if not hand_data:
            return None, None, None

        hand_entity = HandSchema(**hand_data)
        hand = hand_entity.to_domain()

        hand_object_id = hand_data["_id"]  # ✅ Use MongoDB ObjectId for sorting

        # Get previous hand (sorted by `_id` descending)
        prev_hand_data = await collection.find_one(
            {"user_id": user_id, "_id": {"$lt": hand_object_id}},  # ✅ Use `_id`
            sort=[("_id", -1)],
        )
        prev_hand_id = prev_hand_data["id"] if prev_hand_data else None

        # Get next hand (sorted by `_id` ascending)
        next_hand_data = await collection.find_one(
            {"user_id": user_id, "_id": {"$gt": hand_object_id}},  # ✅ Use `_id`
            sort=[("_id", 1)],
        )
        next_hand_id = next_hand_data["id"] if next_hand_data else None

        return hand, prev_hand_id, next_hand_id

    async def delete_all(self, user_id: str) -> None:
        """Delete all hands belonging to a specific user."""
        await self.conn.get_collection(hands_collection_name).delete_many(
            {"user_id": user_id}
        )
