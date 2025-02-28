import json
from typing import List, Optional, Tuple
from pathlib import Path
from asyncio import Lock
from app.hand.domain.hand import Hand
from app.hand.domain.hand_repository import HandRepository


class HandJsonRepository(HandRepository):
    """JSON-based repository for hands (persistent storage)."""

    STORAGE_DIR = Path("hands_storage")
    _locks = {}  # Ensures thread safety

    def __init__(self):
        """Load existing hands from file on startup."""
        self.STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, user_id: str) -> Path:
        """Return the file path for a given user ID."""
        return self.STORAGE_DIR / f"{user_id}.json"

    def _get_lock(self, user_id: str) -> Lock:
        """Return a lock specific to a user, creating one if necessary."""
        if user_id not in self._locks:
            self._locks[user_id] = Lock()
        return self._locks[user_id]

    def _load_hands(self, user_id: str) -> List[Hand]:
        """Load hands from the JSON file."""
        file_path = self._get_file_path(user_id)
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    hands_data = json.load(f)
                    return [
                        Hand.from_primitives(
                            {
                                "id": hand["id"],
                                "user_id": "75565b68-ed1f-11ef-901b-0ade7a4f7cd3",
                                "general_info": hand["general_info"],
                                "table_name": hand["table_name"],
                                "table_type": hand["table_type"],
                                "button_seat": hand["button_seat"],
                                "players": hand["players"],
                                "hero_cards": hand["hero_cards"],
                                "hero_name": hand["hero_name"],
                                "hero_seat": hand["hero_seat"],
                                "actions": hand["actions"],
                                "summary": hand["summary"],
                            }
                        )
                        for hand in hands_data
                    ]
                except json.JSONDecodeError:
                    print("DECODE ERROR")
                    return []
        return []

    def _save_hands(self, user_id: str, hands: List[Hand]) -> None:
        """Save the given hands list to the user's JSON file."""
        file_path = self._get_file_path(user_id)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([hand.to_primitives() for hand in hands], f, indent=4)

    async def create(self, hand: Hand) -> None:
        """Save a hand to the JSON file."""
        async with self._get_lock(hand.user_id):
            hands = self._load_hands(hand.user_id)  # Reload hands before making changes
            if any(
                existing_hand.general_info.room_hand_id
                == hand.general_info.room_hand_id
                for existing_hand in hands
            ):
                return
            hands.append(hand)
            self._save_hands(hand.user_id, hands)

    async def get(self, hand_id: str, user_id: str) -> Optional[Hand]:
        """Retrieve a hand by ID from the JSON file."""
        async with self._get_lock(user_id):
            hands = self._load_hands(
                user_id
            )  # Reload hands from the file to ensure up-to-date data
            for hand in hands:
                if hand.id == hand_id:
                    return hand
        return None

    async def get_all(self, user_id: str) -> List[Hand]:
        """Retrieve all hands for a specific user."""
        async with self._get_lock(user_id):
            return self._load_hands(user_id)

    async def get_with_neighbors(
        self, hand_id: str, user_id: str
    ) -> Tuple[Optional[Hand], Optional[str], Optional[str]]:
        """Retrieve a hand and determine its previous and next hand for the same user."""
        async with self._get_lock(user_id):
            hands = self._load_hands(user_id)

            prev_hand = None
            next_hand = None

            for index, hand in enumerate(hands):
                if hand.id == hand_id:
                    prev_hand = hands[index - 1] if index > 0 else None
                    next_hand = hands[index + 1] if index < len(hands) - 1 else None
                    return (
                        hand,
                        prev_hand.id if prev_hand else None,
                        next_hand.id if next_hand else None,
                    )

        return None, None, None


hand_repository = HandJsonRepository()
