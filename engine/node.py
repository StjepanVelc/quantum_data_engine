# engine/node.py


class QuantumNode:
    """
    Osnovni čvor u Quantum Data Engine-u.

    value      – šta ovaj čvor predstavlja (npr. 'A', korisnik, dokument...)
    amplitude  – koliko je 'aktivno' / vjerovatno (0.0 – 1.0)
    energy     – neka vrsta 'snage' / važnosti
    links      – povezani čvorovi (graf)
    entangled_with – skup čvorova s kojima je kvantno spregnut
    """

    def __init__(self, value, amplitude=0.5, energy=50.0):
        self.value = value
        self.amplitude = amplitude
        self.energy = energy
        self.links = []
        self.entangled_with = set()

        # --- NEW: označava da li čvor predstavlja realni qubit ---
        self.is_qubit = False

    # --- graf funkcije ---

    def link(self, other):
        """Dvosmjerno linkanje čvorova u grafu."""
        if other not in self.links:
            self.links.append(other)
        if self not in other.links:
            other.links.append(self)

    def unlink(self, other):
        """Skidanje veze između čvorova."""
        if other in self.links:
            self.links.remove(other)
        if self in other.links:
            other.links.remove(self)

    # --- helpers ---

    def add_entanglement(self, other):
        """Dodaj kvantno sprezanje s drugim čvorom."""
        if other is self:
            return
        self.entangled_with.add(other)
        other.entangled_with.add(self)

    def clear_entanglement(self):
        """Raskid svih sprezanja za ovaj čvor."""
        for other in list(self.entangled_with):
            other.entangled_with.discard(self)
        self.entangled_with.clear()

    def __repr__(self):
        return f"<Node value={self.value}, amp={self.amplitude:.2f}, energy={self.energy:.1f}>"
