class Qubit:
    """
    Lagani objekt koji predstavlja jedan qubit unutar QuantumRegister-a.
    Nema vlastito stanje – sve je u globalnom kvantnom registru.
    """

    def __init__(self, index, name=None):
        self.index = index
        self.name = name if name else f"Q{index}"

    def __repr__(self):
        return f"<Qubit {self.name} (index={self.index})>"
