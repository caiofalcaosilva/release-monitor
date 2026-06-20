import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import GITHUB_TOKEN

_headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_releases(repo: str) -> list:
    url = f"https://api.github.com/repos/{repo}/releases"
    response = requests.get(url, headers=_headers, params={"per_page": 20}, timeout=10)
    response.raise_for_status()
    return response.json()
