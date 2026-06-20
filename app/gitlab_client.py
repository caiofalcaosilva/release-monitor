from datetime import datetime, timezone

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import GITLAB_TOKEN, GITLAB_URL

_headers = {"PRIVATE-TOKEN": GITLAB_TOKEN} if GITLAB_TOKEN else {}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_releases(repo: str) -> list:
    encoded = repo.replace("/", "%2F")
    url = f"{GITLAB_URL}/api/v4/projects/{encoded}/releases"
    response = requests.get(url, headers=_headers, params={"per_page": 20}, timeout=10)
    response.raise_for_status()

    releases = []
    for r in response.json():
        released_at = r.get("released_at") or r.get("created_at")
        dt = datetime.fromisoformat(released_at.replace("Z", "+00:00"))
        releases.append({
            "id": int(dt.timestamp()),
            "tag_name": r["tag_name"],
            "published_at": released_at,
            "html_url": r.get("_links", {}).get("self", f"{GITLAB_URL}/{repo}/-/releases/{r['tag_name']}"),
            "author": {"login": r.get("author", {}).get("username", "unknown")},
            "assets": r.get("assets", {}).get("links", []),
            "prerelease": r.get("upcoming_release", False),
        })
    return releases
