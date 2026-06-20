import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from app.config import GITLAB_URL, GITLAB_REPOS, REPOS, PYPI_PACKAGES, DOCKER_IMAGES, NPM_PACKAGES
from app import github_client, gitlab_client, pypi_client, docker_client, npm_client
from app.notifier import send_release_notification
from app.state import get_last_release_id, set_last_release, update_last_checked

logger = logging.getLogger(__name__)


def _check_repo(repo: str, state_key: str, releases: list, repo_url: str, source: str):
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
            enriched = {**release, "repo_name": repo, "repo_url": repo_url, "source": source}
            try:
                send_release_notification(enriched)
                set_last_release(state_key, release)
            except Exception:
                logger.exception(f"Error sending notification for {repo} ({release['tag_name']})")
                break

    update_last_checked(state_key)


def _fetch_and_check(name: str, source: str, fetch_fn, state_key: str, url: str):
    logger.info(f"Checking releases for {name} ({source})...")
    try:
        releases = fetch_fn(name)
    except Exception:
        logger.exception(f"Error fetching releases for {name} ({source})")
        return
    if not releases:
        logger.warning(f"No releases found for {name} ({source})")
        return
    _check_repo(name, state_key, releases, url, source)


def check_release():
    for repo in REPOS:
        _fetch_and_check(repo, "github", github_client.get_releases,
                         repo, f"https://github.com/{repo}")

    for repo in GITLAB_REPOS:
        _fetch_and_check(repo, "gitlab", gitlab_client.get_releases,
                         f"gitlab:{repo}", f"{GITLAB_URL}/{repo}")

    for pkg in PYPI_PACKAGES:
        _fetch_and_check(pkg, "pypi", pypi_client.get_releases,
                         f"pypi:{pkg}", f"https://pypi.org/project/{pkg}/")

    for img in DOCKER_IMAGES:
        ns = "library" if "/" not in img else img.split("/", 1)[0]
        img_name = img if "/" not in img else img.split("/", 1)[1]
        _fetch_and_check(img, "docker", docker_client.get_releases,
                         f"docker:{img}", f"https://hub.docker.com/r/{ns}/{img_name}")

    for pkg in NPM_PACKAGES:
        _fetch_and_check(pkg, "npm", npm_client.get_releases,
                         f"npm:{pkg}", f"https://www.npmjs.com/package/{pkg}")


def start_scheduler(interval):
    scheduler = BlockingScheduler()
    scheduler.add_job(check_release, "interval", minutes=interval)

    logger.info(f"Scheduler started. Interval: {interval} minutes.")
    scheduler.start()
