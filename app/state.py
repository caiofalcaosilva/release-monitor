import json
import os
from datetime import datetime, timezone

from app.config import STATE_FILE

_cache: dict | None = None


def _load_from_disk() -> dict:
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
        if "last_release_id" in data:
            return {}
        return data
    except json.JSONDecodeError:
        return {}


def _get_cache() -> dict:
    global _cache
    if _cache is None:
        _cache = _load_from_disk()
    return _cache


def save_state(state: dict):
    global _cache
    _cache = state
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_last_release_id(repo: str):
    entry = _get_cache().get(repo)
    if entry is None:
        return None
    if isinstance(entry, dict):
        return entry.get("id")
    return entry  # backward compat: old format stored int directly


def set_last_release(repo: str, release: dict):
    state = _get_cache()
    existing = state.get(repo)
    base = existing if isinstance(existing, dict) else {}
    state[repo] = {
        **base,
        "id": release["id"],
        "tag_name": release["tag_name"],
        "published_at": release["published_at"],
        "html_url": release["html_url"],
    }
    save_state(state)


def update_last_checked(repo: str):
    state = _get_cache()
    existing = state.get(repo)
    if isinstance(existing, int):
        existing = {"id": existing}
    elif existing is None:
        existing = {}
    state[repo] = {**existing, "last_checked": datetime.now(timezone.utc).isoformat()}
    save_state(state)


def get_all_repos_state() -> dict:
    return dict(_get_cache())
