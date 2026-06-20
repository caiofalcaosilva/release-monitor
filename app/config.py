import os

REPOS        = [r.strip() for r in os.getenv("REPOS", "").split(",") if r.strip()]
GITLAB_REPOS = [r.strip() for r in os.getenv("GITLAB_REPOS", "").split(",") if r.strip()]

INTERVAL_MINUTES = int(os.getenv("INTERVAL_MINUTES", "60"))
IGNORE_PRERELEASE = os.getenv("IGNORE_PRERELEASE", "true").lower() == "true"
GOOGLE_CHAT_WEBHOOK = os.getenv("GOOGLE_CHAT_WEBHOOK")
STATE_FILE = os.getenv("STATE_FILE", "/app/state.json")
TIMEZONE = os.getenv("TIMEZONE", "UTC")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
GITLAB_URL   = os.getenv("GITLAB_URL", "https://gitlab.com").rstrip("/")


if not REPOS and not GITLAB_REPOS:
    raise ValueError("At least one of REPOS or GITLAB_REPOS must be set")

if not GOOGLE_CHAT_WEBHOOK:
    raise ValueError("GOOGLE_CHAT_WEBHOOK environment variable not set")
