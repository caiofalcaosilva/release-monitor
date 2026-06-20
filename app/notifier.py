import requests
from datetime import datetime
from zoneinfo import ZoneInfo

from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import GOOGLE_CHAT_WEBHOOK, IGNORE_PRERELEASE, TIMEZONE

_SOURCE_ICONS = {
    "github": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
    "gitlab": "https://about.gitlab.com/images/press/logo/png/gitlab-icon-rgb.png",
    "pypi":   "https://pypi.org/static/images/logo-small.8998e9d1.svg",
    "docker": "https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png",
    "npm":    "https://static.npmjs.com/338e4905a2684ca96e08c7780fc68412.png",
}

_SOURCE_TITLES = {
    "github": "🚀 New GitHub Release",
    "gitlab": "🦊 New GitLab Release",
    "pypi":   "🐍 New PyPI Release",
    "docker": "🐳 New Docker Image",
    "npm":    "📦 New npm Release",
}

_SOURCE_LABELS = {
    "github": "Repository",
    "gitlab": "Repository",
    "pypi":   "Package",
    "docker": "Image",
    "npm":    "Package",
}


def _detect_source(release: dict) -> str:
    return release.get("source", "github")


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def send_release_notification(release: dict):
    if IGNORE_PRERELEASE and release.get("prerelease"):
        return

    published = datetime.fromisoformat(release["published_at"].replace("Z", "+00:00"))
    published_local = published.astimezone(ZoneInfo(TIMEZONE))
    released_at = published_local.strftime("%d/%m/%Y %H:%M:%S")

    source    = _detect_source(release)
    repo_url  = release.get("repo_url")  or release["html_url"]
    repo_name = release.get("repo_name") or repo_url.split("/")[-1]
    icon_url  = _SOURCE_ICONS.get(source, _SOURCE_ICONS["github"])
    title     = _SOURCE_TITLES.get(source, "🚀 New Release")
    label     = _SOURCE_LABELS.get(source, "Source")

    widgets = [
        {"decoratedText": {"topLabel": label,       "text": repo_name}},
        {"decoratedText": {"topLabel": "Version",   "text": release["tag_name"]}},
        {"decoratedText": {"topLabel": "Released",  "text": f"{released_at} ({TIMEZONE})"}},
    ]

    author = release.get("author", {}).get("login", "")
    if author and author != "unknown":
        widgets.insert(2, {"decoratedText": {"topLabel": "Author", "text": author}})

    assets = release.get("assets", [])
    if assets:
        widgets.append({"decoratedText": {"topLabel": "Assets", "text": f"{len(assets)} files"}})

    payload = {
        "cardsV2": [
            {
                "cardId": "release_card",
                "card": {
                    "header": {
                        "title":    title,
                        "subtitle": repo_name,
                        "imageUrl": icon_url,
                        "imageType": "CIRCLE",
                    },
                    "sections": [
                        {"widgets": widgets},
                        {
                            "widgets": [
                                {
                                    "buttonList": {
                                        "buttons": [
                                            {
                                                "text": "VIEW RELEASE",
                                                "onClick": {"openLink": {"url": release["html_url"]}},
                                            }
                                        ]
                                    }
                                }
                            ]
                        },
                    ],
                },
            }
        ]
    }

    response = requests.post(GOOGLE_CHAT_WEBHOOK, json=payload, timeout=10)
    response.raise_for_status()
