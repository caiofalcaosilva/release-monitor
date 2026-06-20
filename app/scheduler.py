import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from app.config import REPOS
from app.github_client import get_releases
from app.notifier import send_release_notification
from app.state import get_last_release_id, set_last_release, update_last_checked

logger = logging.getLogger(__name__)


def check_release():
    for repo in REPOS:
        logger.info(f"Checking releases for {repo}...")

        try:
            releases = get_releases(repo)
        except Exception:
            logger.exception(f"Error fetching releases for {repo}")
            continue

        if not releases:
            logger.warning(f"No releases found for {repo}")
            continue

        last_id = get_last_release_id(repo)

        if last_id is None:
            logger.info(f"First run for {repo}. Saving current release without notifying.")
            set_last_release(repo, releases[0])
            continue

        new_releases = [r for r in releases if r["id"] > last_id]

        if not new_releases:
            logger.info(f"No new releases for {repo}")
        else:
            logger.info(f"{len(new_releases)} new release(s) detected for {repo}")

            for release in sorted(new_releases, key=lambda r: r["published_at"]):
                try:
                    send_release_notification(release)
                    set_last_release(repo, release)
                except Exception:
                    logger.exception(f"Error sending notification for {repo} ({release['tag_name']})")
                    break

        update_last_checked(repo)


def start_scheduler(interval):
    scheduler = BlockingScheduler()
    scheduler.add_job(check_release, "interval", minutes=interval)

    logger.info(f"Scheduler started. Interval: {interval} minutes.")
    scheduler.start()
