import json


class Snapshot:
    def __init__(self, path="snapshot.json"):
        self.path = path

    def save(self, state):
        """Čuva kompletnu kopiju baze"""
        with open(self.path, "w") as f:
            json.dump(state, f, indent=4)

    def load(self):
        """Učitava cijeli snapshot"""
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
