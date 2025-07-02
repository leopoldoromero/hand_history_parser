import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from app.shared.infrastructure.tasks.remove_guest_hands_task import remove_guests_hands

task_scheduler = BackgroundScheduler()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def sync_remove_guests_hands():
    loop.run_until_complete(remove_guests_hands())


# task_scheduler.add_job(remove_guests_hands, "cron", hour=12, minute=30)

task_scheduler.add_job(sync_remove_guests_hands, "interval", hours=24)
