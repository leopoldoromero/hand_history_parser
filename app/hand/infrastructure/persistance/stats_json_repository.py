import json
from typing import Optional
from pathlib import Path
from asyncio import Lock
from app.hand.domain.stats import Stats
from app.hand.domain.stats_repository import StatsRepository


class StatsJsonRepository(StatsRepository):
    """JSON-based repository for hands (persistent storage)."""

    STORAGE_DIR = Path("stats_storage")
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

    async def persist(self, user_id: str, stats: Stats) -> None:
        """Save the given hands list to the user's JSON file."""
        file_path = self._get_file_path(user_id)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(stats.to_primitives(), f, indent=4)

    async def get_all(self, user_id: str) -> Optional[Stats]:
        """Retrieve a hand by ID from the JSON file."""
        file_path = self._get_file_path(user_id)
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    stats = json.load(f)
                    return stats
                except json.JSONDecodeError:
                    print("DECODE ERROR")
                    return None
        return None


stats_repository = StatsJsonRepository()
