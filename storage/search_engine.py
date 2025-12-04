from storage.indexer import AmplitudeIndex
from storage.energy_index import EnergyIndex
from storage.value_index import ValueIndex


class SearchEngine:
    def __init__(self):
        self.amp = AmplitudeIndex()
        self.energy = EnergyIndex()
        self.value = ValueIndex()

    def rebuild(self, nodes):
        self.amp.rebuild(nodes)
        self.energy.rebuild(nodes)
        self.value.rebuild(nodes)

    def by_amplitude(self, min_amp):
        return self.amp.above(min_amp)

    def by_energy(self, min_energy):
        return self.energy.above(min_energy)

    def by_value(self, value):
        return self.value.get(value)

    def combined(self, min_amp=0, min_energy=0):
        a = set(self.amp.above(min_amp))
        b = set(self.energy.above(min_energy))
        return list(a & b)

    def ranked(self, min_amp=0, min_energy=0):
        res = self.combined(min_amp, min_energy)

        return sorted(res, key=lambda n: n.amplitude + n.energy / 100, reverse=True)
