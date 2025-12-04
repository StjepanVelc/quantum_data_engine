import datetime

LOG_FILE = "log.txt"


def log(message, level="INFO"):
    """
    Jednostavan logger.
    Format: [2025-12-04 17:33:21] [INFO] Poruka
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level}] {message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


def info(msg):
    log(msg, "INFO")


def warn(msg):
    log(msg, "WARN")


def error(msg):
    log(msg, "ERROR")
