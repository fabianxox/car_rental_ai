from apscheduler.schedulers.background import BackgroundScheduler

from app.services.daily_summary_service import get_todays_conversations

from app.ai.daily_summary_ai import generate_daily_summary

from app.services.email_service import send_daily_summary


def daily_summary_job():

    print("RUNNING DAILY SUMMARY JOB")

    conversations = get_todays_conversations()

    summary = generate_daily_summary(conversations)

    send_daily_summary(summary)

    print("DAILY SUMMARY COMPLETED")


scheduler = BackgroundScheduler()

scheduler.add_job(
    daily_summary_job,
    trigger="cron",
    #minute="*/1"
    hour= 18,
    minute=0
)