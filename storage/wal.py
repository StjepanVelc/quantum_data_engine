import json
import time


class WAL:
    def __init__(self, path="wal.log"):
        self.path = path

    def append(self, operation, data):
        """Zapis svake operacije u log"""
        entry = {"ts": time.time(), "op": operation, "data": data}
        with open(self.path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def load(self):
        """Učitava sve zapise iz WAL-a"""
        try:
            with open(self.path, "r") as f:
                return [json.loads(line) for line in f]
        except FileNotFoundError:
            return []

    def clear(self):
        open(self.path, "w").close()
