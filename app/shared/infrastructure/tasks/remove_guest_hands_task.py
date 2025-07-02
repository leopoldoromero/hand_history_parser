import time
from app.hand.application.guest_hands_remover import GuestHandsRemover
from app.shared.infrastructure.di_container import get_dependency


async def remove_guests_hands(
    hand_remover: GuestHandsRemover = get_dependency("guest_hands_remover"),
):
    await hand_remover.execute()
    print(f"Task executed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
