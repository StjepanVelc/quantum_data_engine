from .wal import WAL
from .snapshot import Snapshot
from utils.hashing import hash_state


class StorageEngine:
    def __init__(self):
        self.primary = {}
        self.shadow = {}  # rezervno spremište
        self.wal = WAL()  # write ahead log
        self.snapshot = Snapshot()  # snapshot engine

    def write(self, key, value):
        self.primary[key] = value
        self.wal.append("SET", (key, value))

    def read(self, key):
        return self.primary.get(key)

    def delete(self, key):
        self.primary.pop(key, None)
        self.wal.append("DELETE", key)

    def commit(self):
        """Snima stanje u snapshot i briše WAL"""
        self.snapshot.save(self.primary)
        self.wal.clear()

    def recover(self):
        """Obnavlja stanje iz snapshot-a"""
        self.primary = self.snapshot.load()
