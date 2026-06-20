import re
from datetime import datetime, timezone

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

_PRERELEASE_RE = re.compile(r"(a|b|rc|alpha|beta|dev|post)\d*", re.IGNORECASE)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_releases(package: str) -> list:
    url = f"https://pypi.org/pypi/{package}/json"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    author = data["info"].get("author") or "unknown"
    releases = []

    for version, files in data.get("releases", {}).items():
        if not files:
            continue
        upload_time = files[0].get("upload_time", "")
        if not upload_time:
            continue
        dt = datetime.fromisoformat(upload_time).replace(tzinfo=timezone.utc)
        releases.append({
            "id": int(dt.timestamp()),
            "tag_name": version,
            "published_at": dt.isoformat(),
            "html_url": f"https://pypi.org/project/{package}/{version}/",
            "author": {"login": author},
            "assets": files,
            "prerelease": bool(_PRERELEASE_RE.search(version)),
        })

    return sorted(releases, key=lambda r: r["id"], reverse=True)
