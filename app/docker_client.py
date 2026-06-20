import re
from datetime import datetime

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import DOCKER_HUB_TOKEN

_SKIP_TAGS = {"latest", "stable", "edge", "main", "master", "develop", "nightly"}
_VERSION_RE = re.compile(r"^v?\d+(\.\d+)*([._-][a-z0-9]+)*$", re.IGNORECASE)
_PRERELEASE_RE = re.compile(r"[-._](alpha|beta|rc|dev|pre)", re.IGNORECASE)

_headers = {"Authorization": f"Bearer {DOCKER_HUB_TOKEN}"} if DOCKER_HUB_TOKEN else {}


def _split_image(image: str) -> tuple[str, str]:
    if "/" not in image:
        return "library", image
    namespace, name = image.split("/", 1)
    return namespace, name


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_releases(image: str) -> list:
    namespace, name = _split_image(image)
    url = f"https://hub.docker.com/v2/repositories/{namespace}/{name}/tags"
    response = requests.get(
        url, headers=_headers,
        params={"ordering": "last_updated", "page_size": 25},
        timeout=10,
    )
    response.raise_for_status()

    releases = []
    for tag in response.json().get("results", []):
        tag_name = tag["name"]
        if tag_name.lower() in _SKIP_TAGS or not _VERSION_RE.match(tag_name):
            continue
        last_updated = tag.get("last_updated", "")
        if not last_updated:
            continue
        dt = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
        releases.append({
            "id": int(dt.timestamp()),
            "tag_name": tag_name,
            "published_at": last_updated,
            "html_url": f"https://hub.docker.com/r/{namespace}/{name}/tags?name={tag_name}",
            "author": {"login": tag.get("last_updater_username") or "unknown"},
            "assets": [],
            "prerelease": bool(_PRERELEASE_RE.search(tag_name)),
        })

    return releases  # already newest-first from API ordering
