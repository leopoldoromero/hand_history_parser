from apscheduler.schedulers.background import BackgroundScheduler
from app.shared.infrastructure.tasks.remove_guest_hands_task import remove_guests_hands

task_scheduler = BackgroundScheduler()

task_scheduler.add_job(remove_guests_hands, "cron", hour=12, minute=30)

# task_scheduler.add_job(remove_guests_hands, "interval", seconds=5)
