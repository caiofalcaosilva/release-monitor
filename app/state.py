import json
import os

from app.config import STATE_FILE


def load_state() -> dict:
    if not os.path.exists(STATE_FILE):
        return {}

    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)

        # migração automática do formato antigo
        if "last_release_id" in data:
            return {}

        return data

    except json.JSONDecodeError:
        return {}


def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_last_release_id(repo: str):
    state = load_state()
    return state.get(repo)


def set_last_release_id(repo: str, release_id: int):
    state = load_state()
    state[repo] = release_id
    save_state(state)