from engine.quantum_ops import QuantumOps
from engine.stabilizer import Stabilizer


class QuantumGraph:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def connect(self, node_a, node_b):
        node_a.link(node_b)

    def disconnect(self, node_a, node_b):
        node_a.unlink(node_b)

    def decay_all(self, rate=0.02):
        """Globalna decoherence simulacija."""
        QuantumOps.decoherence(self.nodes, rate)

    def stabilize(self):
        """Balansira čvorove u grafu."""
        Stabilizer.stabilize_nodes(self.nodes)

    def purge_dead(self):
        """Uklanja 'mrtve' čvorove."""
        alive = []
        for node in self.nodes:
            if node.energy > 1 and node.amplitude > 0.05:
                alive.append(node)

        removed = len(self.nodes) - len(alive)
        self.nodes = alive

        if removed > 0:
            print(f"[Graph] Removed {removed} dead nodes.")

    def __repr__(self):
        return f"<Graph nodes={len(self.nodes)}>"
