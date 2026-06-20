# Release Monitor

![Python](https://img.shields.io/badge/python-3.12-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Lightweight Python service that monitors software sources for new releases and sends structured notifications to Google Chat.

Supports **GitHub**, **GitLab**, **PyPI**, **Docker Hub**, and **npm** — any combination, all in a single instance.

---

## Features

- Monitor **multiple sources** simultaneously (GitHub, GitLab, PyPI, Docker Hub, npm)
- Automatic **new release detection** with multi-release catch-up (no missed versions)
- Structured **Google Chat notifications** with source-aware title, icon, and fields
- **Browser-based setup wizard** — no manual `.env` editing required
- **Live status dashboard** at `localhost:8099` with per-source badges
- **UI in three languages**: English, Português, Español
- Configurable check interval and timezone
- Persistent state file to prevent duplicate notifications
- Automatic **retry with exponential backoff** on API errors
- Containerized with Docker / Docker Compose
- Simple commands via **Makefile**

---

## How It Works

On startup, a browser-based setup wizard opens at `http://localhost:8099`.  
Fill in the sources you want to monitor and your Google Chat webhook URL, then click **Save & Start**.

From that point on, the scheduler runs in the background at the configured interval, querying each source's API. When a new version is detected, a Google Chat card is sent:

- Source name and icon (GitHub / GitLab / PyPI / Docker Hub / npm)
- Package or repository name
- Version tag
- Author / maintainer
- Release date (in your configured timezone)
- Direct link to the release page

After setup, the same `localhost:8099` URL shows a **live status dashboard** with the last detected version and last check time for each monitored source.

---

## Supported Sources

| Source | What is monitored | Auth (optional) |
|---|---|---|
| **GitHub** | Repository releases (`owner/repo`) | `GITHUB_TOKEN` — raises limit from 60 to 5,000 req/h |
| **GitLab** | Repository releases (`owner/repo`) | `GITLAB_TOKEN` — required for private repos |
| **PyPI** | Package versions | — (public API, no auth needed) |
| **Docker Hub** | Versioned image tags (`image` or `user/image`) | `DOCKER_HUB_TOKEN` — required for private images |
| **npm** | Package versions (plain or `@scope/package`) | `NPM_TOKEN` — required for private packages |

> At least one source must be configured.

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/caiofalcaosilva/release-monitor.git
cd release-monitor
```

### 2. Run with Docker

```bash
make build
make up
```

Open `http://localhost:8099` in your browser and complete the setup wizard.

### 3. Run locally (Python 3.12+)

```bash
make install
make dev
```

The wizard opens automatically in your default browser.

---

## Configuration

Configuration is handled through the setup wizard at `http://localhost:8099`.  
A `.env` file is generated automatically on save.

You can also create or edit the file manually:

```bash
cp .env.example .env
```

### Environment Variables

| Variable | Description | Required |
|---|---|---|
| `REPOS` | GitHub repos, comma-separated (`owner/repo`) | At least one source |
| `GITLAB_REPOS` | GitLab repos, comma-separated (`owner/repo`) | At least one source |
| `PYPI_PACKAGES` | PyPI package names, comma-separated | At least one source |
| `DOCKER_IMAGES` | Docker Hub images, comma-separated | At least one source |
| `NPM_PACKAGES` | npm package names, comma-separated | At least one source |
| `GOOGLE_CHAT_WEBHOOK` | Google Chat incoming webhook URL | **Yes** |
| `INTERVAL_MINUTES` | How often to check for new releases (default: `60`) | No |
| `IGNORE_PRERELEASE` | Skip pre-releases (default: `true`) | No |
| `TIMEZONE` | Timezone for notification timestamps (default: `UTC`) | No |
| `STATE_FILE` | Path to the state persistence file (default: `/app/data/state.json`) | No |
| `GITHUB_TOKEN` | GitHub Personal Access Token | No |
| `GITLAB_TOKEN` | GitLab Personal Access Token | No |
| `GITLAB_URL` | GitLab instance URL (default: `https://gitlab.com`) | No |
| `DOCKER_HUB_TOKEN` | Docker Hub access token | No |
| `NPM_TOKEN` | npm access token | No |

### Example `.env`

```env
# Sources — at least one required
REPOS=caiofalcaosilva/release-monitor,openai/openai-python
PYPI_PACKAGES=requests,django
DOCKER_IMAGES=nginx
NPM_PACKAGES=express

# Notifications
GOOGLE_CHAT_WEBHOOK=https://chat.googleapis.com/v1/spaces/XXX/messages?key=XXX&token=XXX

# Schedule
INTERVAL_MINUTES=60
IGNORE_PRERELEASE=true
TIMEZONE=America/Sao_Paulo
```

---

## Makefile Commands

### Docker

| Command | Description |
|---|---|
| `make build` | Build the Docker image |
| `make up` | Start container in background |
| `make down` | Stop container |
| `make restart` | Restart container |
| `make rebuild` | Rebuild image and restart |
| `make logs` | Follow container logs |
| `make ps` | Show running container status |

### Development

| Command | Description |
|---|---|
| `make install` | Install Python dependencies |
| `make dev` | Run the application locally |

### Maintenance

| Command | Description |
|---|---|
| `make clean` | Remove containers and volumes |
| `make prune` | Prune unused Docker resources |

---

## Project Structure

```
release-monitor/
│
├── app/
│   ├── __main__.py        # Entry point (python -m app)
│   ├── main.py            # Logging setup and scheduler start
│   ├── config.py          # Environment variable loading and validation
│   ├── scheduler.py       # Periodic check loop for all sources
│   ├── state.py           # In-memory + on-disk state (last seen release IDs)
│   ├── notifier.py        # Google Chat card builder and sender
│   ├── setup_wizard.py    # Browser-based HTTP setup server (port 8099)
│   ├── github_client.py   # GitHub Releases API client
│   ├── gitlab_client.py   # GitLab Releases API client
│   ├── pypi_client.py     # PyPI JSON API client
│   ├── docker_client.py   # Docker Hub Tags API client
│   ├── npm_client.py      # npm Registry API client
│   └── templates/
│       ├── setup.html     # Setup wizard and reconfigure page
│       ├── status.html    # Live status dashboard
│       └── logo.svg       # App icon (served as favicon)
│
├── dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── .env.example
├── README.md
└── LICENSE
```

---

## License

This project is licensed under the MIT License.
