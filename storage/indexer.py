class AmplitudeIndex:
    """
    Indeksira čvorove prema amplitude vrijednosti.

    Omogućava:
    - pretragu stabilnih čvorova
    - detekciju haotičnih čvorova
    - threshold-based selekciju
    - sortiranje čvorova po amplitude
    """

    def __init__(self):
        self.index = []  # lista čvorova (držimo reference na node objekte)

    def rebuild(self, nodes):
        """Potpuno rekreira indeks iz liste čvorova."""
        self.index = list(nodes)
        self.index.sort(key=lambda n: n.amplitude)

    def top_stable(self, k=3):
        """Vraća k najstabilnijih čvorova (najveća amplitude)."""
        return self.index[-k:]

    def most_unstable(self, k=3):
        """Vraća k najnestabilnijih čvorova (najmanja amplitude)."""
        return self.index[:k]

    def above(self, threshold):
        """Vraća sve čvorove iznad zadanog amplitude praga."""
        return [n for n in self.index if n.amplitude >= threshold]

    def below(self, threshold):
        """Vraća sve čvorove ispod praga."""
        return [n for n in self.index if n.amplitude < threshold]
