import os

VIDEO_ID = os.environ.get("VIDEO_ID")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

SNAPSHOT_PATH = os.environ.get(
    "SNAPSHOT_PATH",
    os.path.join(os.path.dirname(__file__), "data", "snapshot.json"),
)

MAX_COMMENTS = int(os.environ.get("MAX_COMMENTS", "5000"))

COOKIES_FILE = os.environ.get("COOKIES_FILE")

NOTIFY_MODIFIED = os.environ.get("NOTIFY_MODIFIED", "true").lower() == "true"
