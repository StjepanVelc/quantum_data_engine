import math
import random


class QuantumOps:
    """
    Kvantne operacije nad čvorovima.
    Ovo NIJE fizika, ali simulira kvantno ponašanje:
    - amplitude 0–1
    - superpozicija
    - sprezanje (entanglement)
    - mjerenje (collapse)
    - decoherence
    - noise
    """

    # --- pomoćna funkcija ---
    @staticmethod
    def _clamp(node):
        node.amplitude = max(0.0, min(1.0, node.amplitude))

    # --- amplitude shift ---
    @staticmethod
    def shift_amplitude(node, delta):
        node.amplitude += delta
        QuantumOps._clamp(node)
        return node.amplitude

    # --- decoherence ---
    @staticmethod
    def decoherence(nodes, rate=0.02):
        """Globalno slabljenje sistema."""
        for n in nodes:
            n.amplitude *= 1.0 - rate
            n.energy *= 1.0 - rate * 0.5
            QuantumOps._clamp(n)

    # --- vizualna superpozicija (demo) ---
    @staticmethod
    def superposition(node, alt):
        return (node.value, alt)

    # --- entanglement ---
    @staticmethod
    def entangle(a, b):
        """
        Kvantno sprezanje dva čvora.
        Samo povezujemo da collapse jednog utiče na drugog.
        """
        a.add_entanglement(b)
        b.add_entanglement(a)

    # --- collapse ---
    @staticmethod
    def collapse(node, basis=("0", "1")):
        """
        Mjerenje čvora:
        - amplitude je vjerovatnoća za '1'
        - collapse daje '0' ili '1'
        - amplitude postaje 1.0 ili 0.0
        - spregnuti čvorovi (entangled) prate isti ishod
        """
        p1 = node.amplitude
        r = random.random()

        outcome = basis[1] if r < p1 else basis[0]

        # collapse ovog čvora
        node.amplitude = 1.0 if outcome == basis[1] else 0.0
        node.energy *= 0.85

        # collapse spregnutih čvorova
        for other in node.entangled_with:
            other.amplitude = node.amplitude
            other.energy *= 0.90

        return outcome

    # --- noise ---
    @staticmethod
    def inject_noise(node, strength=0.05):
        """
        Šum koji malo poremeti amplitude.
        """
        node.amplitude += (random.random() - 0.5) * strength
        QuantumOps._clamp(node)
