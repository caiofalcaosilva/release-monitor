# Release Monitor

![Python](https://img.shields.io/badge/python-3.12-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Lightweight Python service that monitors repositories for new releases and sends notifications to Google Chat.

It periodically checks repositories for new versions and sends structured notifications when a new release is detected.

## Features

* Monitor **multiple repositories**
* Automatic **release detection**
* Notifications sent to Google Chat
* Configurable **check interval**
* Timezone support
* Avoid duplicate notifications using a persistent state file
* Containerized with Docker
* Simple commands using **Makefile**

---

# How It Works

The service periodically queries the GitHub API to check the latest release of configured repositories.

When a new release is detected, a notification is sent to Google Chat including:

* Repository name
* Version tag
* Author
* Release date
* Number of assets
* Link to the release

---

# Installation

## Clone the repository

```bash
git clone https://github.com/YOUR-USER/release-monitor.git
cd release-monitor
```

---

# Configuration

Create your environment file:

```bash
cp .env.example .env
```

Edit `.env` with your configuration.

Example:

```
REPOS=owner/repository
INTERVAL_MINUTES=5
IGNORE_PRERELEASE=true
GOOGLE_CHAT_WEBHOOK=https://chat.googleapis.com/...
STATE_FILE=/app/data/state.json
TIMEZONE=UTC
```

---

# Running with Docker

Build the image:

```bash
make build
```

Start the service:

```bash
make up
```

Stop the service:

```bash
make down
```

Restart the service:

```bash
make restart
```

View logs:

```bash
make logs
```

Check running containers:

```bash
make ps
```

Rebuild and restart:

```bash
make rebuild
```

---

# Running Locally (Python)

Install dependencies:

```bash
make install
```

Run the application:

```bash
make dev
```

---

# Maintenance

Clean containers and volumes:

```bash
make clean
```

Prune unused Docker resources:

```bash
make prune
```

---

# Project Structure

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
├── Makefile
├── requirements.txt
├── .env.example
├── README.md
└── LICENSE
```

---

# License

This project is licensed under the MIT License.
