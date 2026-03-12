import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from app.config import REPOS
from app.github_client import get_latest_release
from app.notifier import send_release_notification
from app.state import get_last_release_id, set_last_release_id

logger = logging.getLogger(__name__)


def check_release():
    for repo in REPOS:
        logger.info(f"Checking latest release for {repo}...")

        try:
            release = get_latest_release(repo)
        except Exception:
            logger.exception(f"Error fetching latest release for {repo}")
            continue

        if not release:
            logger.warning(f"No release data returned for {repo}")
            continue

        latest_id = release["id"]
        last_id = get_last_release_id(repo)

        if last_id is None:
            logger.info(f"First run for {repo}. Saving current release without notifying.")
            set_last_release_id(repo, latest_id)
            continue

        if latest_id != last_id:
            logger.info(f"New release detected for {repo}")

            try:
                send_release_notification(release)
                set_last_release_id(repo, latest_id)
            except Exception:
                logger.exception(f"Error sending notification for {repo}")
        else:
            logger.info(f"No new release for {repo}")


def start_scheduler(interval):
    scheduler = BlockingScheduler()
    scheduler.add_job(check_release, "interval", minutes=interval)

    logger.info(f"Scheduler started. Interval: {interval} minutes.")
    scheduler.start()
