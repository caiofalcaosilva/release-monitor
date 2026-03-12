import logging
import signal
import sys

import requests

from app.config import GOOGLE_CHAT_WEBHOOK, INTERVAL_MINUTES
from app.scheduler import start_scheduler

logger = logging.getLogger(__name__)


def validate_google_webhook():
    try:
        response = requests.post(
            GOOGLE_CHAT_WEBHOOK,
            json={"text": "✅ Webhook validation message"},
            timeout=10,
        )

        response.raise_for_status()

        logger.info("Google Chat webhook validated successfully.")

    except Exception as e:
        logger.error("Invalid Google Chat webhook URL.")
        raise SystemExit(1) from e


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def handle_shutdown(signum, frame):
    logging.info("Shutdown signal received. Stopping application gracefully...")
    sys.exit(0)


def main():
    validate_google_webhook()
    setup_logging()

    logging.info("Starting WA-JS release monitor...")
    logging.info(f"Checking interval: {INTERVAL_MINUTES} minutes")

    # Graceful shutdown (Docker friendly)
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    start_scheduler(INTERVAL_MINUTES)


if __name__ == "__main__":
    main()