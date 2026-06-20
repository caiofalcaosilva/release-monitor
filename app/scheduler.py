import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from app.config import GITLAB_URL, GITLAB_REPOS, REPOS
from app import github_client, gitlab_client
from app.notifier import send_release_notification
from app.state import get_last_release_id, set_last_release, update_last_checked

logger = logging.getLogger(__name__)


def _check_repo(repo: str, state_key: str, releases: list, repo_url: str):
    last_id = get_last_release_id(state_key)

    if last_id is None:
        logger.info(f"First run for {repo}. Saving current release without notifying.")
        set_last_release(state_key, releases[0])
        update_last_checked(state_key)
        return

    new_releases = [r for r in releases if r["id"] > last_id]

    if not new_releases:
        logger.info(f"No new releases for {repo}")
    else:
        logger.info(f"{len(new_releases)} new release(s) detected for {repo}")

        for release in sorted(new_releases, key=lambda r: r["published_at"]):
            enriched = {**release, "repo_name": repo, "repo_url": repo_url}
            try:
                send_release_notification(enriched)
                set_last_release(state_key, release)
            except Exception:
                logger.exception(f"Error sending notification for {repo} ({release['tag_name']})")
                break

    update_last_checked(state_key)


def check_release():
    for repo in REPOS:
        logger.info(f"Checking releases for {repo} (github)...")
        try:
            releases = github_client.get_releases(repo)
        except Exception:
            logger.exception(f"Error fetching releases for {repo} (github)")
            continue

        if not releases:
            logger.warning(f"No releases found for {repo} (github)")
            continue

        _check_repo(repo, repo, releases, f"https://github.com/{repo}")

    for repo in GITLAB_REPOS:
        logger.info(f"Checking releases for {repo} (gitlab)...")
        try:
            releases = gitlab_client.get_releases(repo)
        except Exception:
            logger.exception(f"Error fetching releases for {repo} (gitlab)")
            continue

        if not releases:
            logger.warning(f"No releases found for {repo} (gitlab)")
            continue

        _check_repo(repo, f"gitlab:{repo}", releases, f"{GITLAB_URL}/{repo}")


def start_scheduler(interval):
    scheduler = BlockingScheduler()
    scheduler.add_job(check_release, "interval", minutes=interval)

    logger.info(f"Scheduler started. Interval: {interval} minutes.")
    scheduler.start()
