# Release Monitor

![Python](https://img.shields.io/badge/python-3.12-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Lightweight Python service that monitors repositories for new releases and sends notifications to Google Chat.
It automatically checks repositories for new versions and notifies your team in real time.

## Features

* Monitor **multiple repositories**
* Automatic **release detection**
* Notifications sent to **Google Chat**
* Configurable **check interval**
* Support for **timezone configuration**
* Avoids duplicate notifications using a persistent state file
* Retry logic for reliability
* Containerized with **Docker**

## How It Works

The service periodically checks the API of a repository host for the latest release.
If a new release is detected, it sends a structured notification to a Google Chat webhook with details such as:

* Repository
* Version
* Author
* Release date
* Number of assets
* Direct link to the release

## Example Notification

A notification sent to Google Chat includes:

* 🚀 Release title
* 📦 Repository name
* 🏷 Version tag
* 👤 Author
* 📅 Release date
* 🔗 Link to the release page

## Installation

### Clone the repository

```bash
git clone https://github.com/YOUR-USER/release-monitor.git
cd release-monitor
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create environment variables

Copy the example file:

```bash
cp .env.example .env
```

Edit `.env` with your configuration.

## Environment Variables

Example configuration:

```
GOOGLE_CHAT_WEBHOOK=https://chat.googleapis.com/...
REPOS=owner/repo1,owner/repo2
INTERVAL_MINUTES=5
TIMEZONE=UTC
IGNORE_PRERELEASE=true
STATE_FILE=/app/data/state.json
```

| Variable            | Description                                     |
| ------------------- | ----------------------------------------------- |
| GOOGLE_CHAT_WEBHOOK | Google Chat webhook URL                         |
| REPOS               | Comma-separated list of repositories to monitor |
| INTERVAL_MINUTES    | How often to check for new releases             |
| TIMEZONE            | Timezone used for release timestamps            |
| IGNORE_PRERELEASE   | Ignore pre-release versions                     |
| STATE_FILE          | File used to store last processed releases      |

## Running with Python

```bash
python -m app.main
```

## Running with Docker

Build the image:

```bash
docker build -t release-monitor .
```

Run the container:

```bash
docker run --env-file .env release-monitor
```

## Running with Docker Compose

```bash
docker compose up -d
```

Example `docker-compose.yml`:

```
version: "3.8"

services:
  release-monitor:
    build: .
    container_name: release-monitor
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./data:/app/data
```

## Project Structure

```
release-monitor
│
├── app
│   ├── config.py
│   ├── github_client.py
│   ├── notifier.py
│   ├── scheduler.py
│   ├── state.py
│   └── main.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── README.md
└── LICENSE
```

## License

This project is licensed under the MIT License.
