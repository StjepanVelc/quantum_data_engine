from storage.wal import WAL
from storage.snapshot import Snapshot
from utils.hashing import hash_state


class StorageEngine:
    def __init__(self):
        self.state = {}
        self.wal = WAL()
        self.snap = Snapshot()
        self.last_hash = None

        # Ako postoji snapshot → učitaj
        self.state = self.snap.load()

        # Ako postoji WAL → primijeni sve operacije
        for entry in self.wal.load():
            self.apply(entry["op"], entry["data"])

    def apply(self, operation, data):
        """Primjena jedne operacije nad stanjem"""
        if operation == "SET":
            key, value = data
            self.state[key] = value

        elif operation == "DELETE":
            key = data
            self.state.pop(key, None)

    def set(self, key, value):
        """Dodaje podatak u stanje + zapisuje u WAL"""
        self.wal.append("SET", (key, value))
        self.apply("SET", (key, value))

    def delete(self, key):
        self.wal.append("DELETE", key)
        self.apply("DELETE", key)

    def commit_snapshot(self):
        """Snapshot + validacijski hash"""
        self.snap.save(self.state)
        self.last_hash = hash_state(self.state)
        self.wal.clear()
        return self.last_hash
