import requests
from datetime import datetime
from zoneinfo import ZoneInfo

from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import GOOGLE_CHAT_WEBHOOK, IGNORE_PRERELEASE, TIMEZONE

_SOURCE_ICONS = {
    "gitlab": "https://about.gitlab.com/images/press/logo/png/gitlab-icon-rgb.png",
    "github": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
}


def _detect_source(release: dict) -> str:
    if "repo_url" in release and "gitlab" in release["repo_url"]:
        return "gitlab"
    return "github"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def send_release_notification(release: dict):
    if IGNORE_PRERELEASE and release.get("prerelease"):
        return

    published = datetime.fromisoformat(release["published_at"].replace("Z", "+00:00"))
    published_local = published.astimezone(ZoneInfo(TIMEZONE))
    released_at = published_local.strftime("%d/%m/%Y %H:%M:%S")

    source = _detect_source(release)
    repo_url  = release.get("repo_url")  or release["html_url"].split("/releases")[0]
    repo_name = release.get("repo_name") or repo_url.split(f"{source}.com/")[-1]
    icon_url  = _SOURCE_ICONS[source]
    title     = f"🚀 New {'GitLab' if source == 'gitlab' else 'GitHub'} Release"

    payload = {
        "cardsV2": [
            {
                "cardId": "release_card",
                "card": {
                    "header": {
                        "title": title,
                        "subtitle": repo_name,
                        "imageUrl": icon_url,
                        "imageType": "CIRCLE",
                    },
                    "sections": [
                        {
                            "widgets": [
                                {"decoratedText": {"topLabel": "Repository", "text": repo_name}},
                                {"decoratedText": {"topLabel": "Version",    "text": release["tag_name"]}},
                                {"decoratedText": {"topLabel": "Author",     "text": release["author"]["login"]}},
                                {"decoratedText": {"topLabel": "Released",   "text": f"{released_at} ({TIMEZONE})"}},
                                {"decoratedText": {"topLabel": "Assets",     "text": f"{len(release.get('assets', []))} files"}},
                            ]
                        },
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
