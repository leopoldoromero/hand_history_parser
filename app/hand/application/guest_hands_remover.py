from app.user.domain.user_repository import UserRepository
from app.hand.domain.hand_repository import HandRepository


class GuestHandsRemover:
    def __init__(
        self, hands_repository: HandRepository, user_repository: UserRepository
    ):
        self.hands_repository = hands_repository
        self.user_repository = user_repository

    async def execute(self) -> None:
        hands = await self.hands_repository.get_all_by_criteria(None)

        for hand in hands:
            user = await self.user_repository.get(hand.user_id)
            if not user:
                await self.hands_repository.delete_all(hand.user_id)
