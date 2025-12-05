from engine.quantum_core.qubit import Qubit


class NodeQubitBinder:
    """
    Veže graf čvorove na qubite Q0–Q5.
    Svaki čvor dobije:
        node.qubit_index
        node.qubit = Qubit(...)
    """

    def __init__(self, num_qubits=6):
        self.num_qubits = num_qubits

    def bind(self, graph):
        """
        Dodjeljuje qubit index svakom node-u redom kako je dodan u graf.
        """
        if len(graph.nodes) < self.num_qubits:
            raise ValueError(
                f"Graph has {len(graph.nodes)} nodes, but {self.num_qubits} qubits are required."
            )

        for i, node in enumerate(graph.nodes[: self.num_qubits]):
            node.is_qubit = True
            node.qubit_index = i
            node.qubit = Qubit(i, f"Q{i}")

        # Ako ima viška nodeova — oni nisu qubitovi
        for node in graph.nodes[self.num_qubits :]:
            node.is_qubit = False
            node.qubit_index = None
            node.qubit = None

        return graph
