class ValueIndex:
    def __init__(self):
        self.map = {}

    def rebuild(self, nodes):
        self.map = {n.value: n for n in nodes}

    def get(self, value):
        return self.map.get(value)
