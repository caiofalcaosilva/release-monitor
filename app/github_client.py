import requests
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_latest_release(repo: str):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()