import os

REPOS = [repo.strip() for repo in os.getenv("REPOS", "").split(",") if repo.strip()]
INTERVAL_MINUTES = int(os.getenv("INTERVAL_MINUTES", "60"))
IGNORE_PRERELEASE = os.getenv("IGNORE_PRERELEASE", "true").lower() == "true"
GOOGLE_CHAT_WEBHOOK = os.getenv("GOOGLE_CHAT_WEBHOOK")
STATE_FILE = os.getenv("STATE_FILE", "/app/state.json")
TIMEZONE = os.getenv("TIMEZONE", "UTC")


if not REPOS:
    raise ValueError("REPO environment variable not set")

if not GOOGLE_CHAT_WEBHOOK:
    raise ValueError("GOOGLE_CHAT_WEBHOOK environment variable not set")