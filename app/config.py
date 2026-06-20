import os

REPOS         = [r.strip() for r in os.getenv("REPOS", "").split(",") if r.strip()]
GITLAB_REPOS  = [r.strip() for r in os.getenv("GITLAB_REPOS", "").split(",") if r.strip()]
PYPI_PACKAGES = [p.strip() for p in os.getenv("PYPI_PACKAGES", "").split(",") if p.strip()]
DOCKER_IMAGES = [i.strip() for i in os.getenv("DOCKER_IMAGES", "").split(",") if i.strip()]
NPM_PACKAGES  = [p.strip() for p in os.getenv("NPM_PACKAGES", "").split(",") if p.strip()]

INTERVAL_MINUTES    = int(os.getenv("INTERVAL_MINUTES", "60"))
IGNORE_PRERELEASE   = os.getenv("IGNORE_PRERELEASE", "true").lower() == "true"
GOOGLE_CHAT_WEBHOOK = os.getenv("GOOGLE_CHAT_WEBHOOK")
STATE_FILE          = os.getenv("STATE_FILE", "/app/state.json")
TIMEZONE            = os.getenv("TIMEZONE", "UTC")
GITHUB_TOKEN        = os.getenv("GITHUB_TOKEN")
GITLAB_TOKEN        = os.getenv("GITLAB_TOKEN")
GITLAB_URL          = os.getenv("GITLAB_URL", "https://gitlab.com").rstrip("/")
NPM_TOKEN           = os.getenv("NPM_TOKEN")
DOCKER_HUB_TOKEN    = os.getenv("DOCKER_HUB_TOKEN")


if not any([REPOS, GITLAB_REPOS, PYPI_PACKAGES, DOCKER_IMAGES, NPM_PACKAGES]):
    raise ValueError(
        "At least one source must be configured: "
        "REPOS, GITLAB_REPOS, PYPI_PACKAGES, DOCKER_IMAGES, or NPM_PACKAGES"
    )

if not GOOGLE_CHAT_WEBHOOK:
    raise ValueError("GOOGLE_CHAT_WEBHOOK environment variable not set")
