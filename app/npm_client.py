import re
from datetime import datetime

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import NPM_TOKEN

_PRERELEASE_RE = re.compile(r"[-+](alpha|beta|rc|dev|pre|canary)", re.IGNORECASE)
_headers = {"Authorization": f"Bearer {NPM_TOKEN}"} if NPM_TOKEN else {}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_releases(package: str) -> list:
    encoded = package.replace("/", "%2F")
    url = f"https://registry.npmjs.org/{encoded}"
    response = requests.get(url, headers=_headers, timeout=15)
    response.raise_for_status()
    data = response.json()

    maintainer = (data.get("maintainers") or [{}])[0].get("name", "unknown")
    times = data.get("time", {})

    releases = []
    for version, timestamp in times.items():
        if version in ("created", "modified"):
            continue
        try:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            continue
        releases.append({
            "id": int(dt.timestamp()),
            "tag_name": version,
            "published_at": dt.isoformat(),
            "html_url": f"https://www.npmjs.com/package/{package}/v/{version}",
            "author": {"login": maintainer},
            "assets": [],
            "prerelease": bool(_PRERELEASE_RE.search(version)),
        })

    return sorted(releases, key=lambda r: r["id"], reverse=True)[:30]
