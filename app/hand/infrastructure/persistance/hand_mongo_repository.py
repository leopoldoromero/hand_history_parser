from app.shared.infrastructure.db import hands_collection
from app.hand.infrastructure.hand_schema import HandSchema
from app.hand.domain.hand import HandRepository
from app.hand.domain.hand import Hand

class HandMongoRepository(HandRepository):
    """MongoDB implementation of UserRepository."""
    async def create(self, hand: Hand) -> None:
        """Insert a new hand into MongoDB."""
        await hands_collection.insert_one(HandSchema.from_domain(hand).model_dump())

    async def get(self, hand_id: str) -> Hand:
        """Retrieve a hand by ID."""
        hand_data = await hands_collection.find_one({"id": hand_id})
        if hand_data:
            return HandSchema(**hand_data).model_dump()

        return None
    
    async def get_all(self, user_id: str) -> list[Hand]:
        """Retrieve all hands belonging to a specific user."""
        hands_cursor = hands_collection.find({"user_id": user_id})
        hands_list = await hands_cursor.to_list(length=None)
        return [HandSchema(**hand).model_dump() for hand in hands_list]
