class EnergyIndex:
    def __init__(self):
        self.index = []

    def rebuild(self, nodes):
        self.index = list(nodes)
        self.index.sort(key=lambda n: n.energy)

    def above(self, min_energy):
        return [n for n in self.index if n.energy >= min_energy]
