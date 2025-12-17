import numpy as np


class HeatmapView:
    def __init__(self, ax, graph):
        self.ax = ax
        self.graph = graph

        n = graph.simulation.num_qubits
        self.data = np.zeros((n, n))

        self.im = ax.imshow(
            self.data,
            vmin=0.0,
            vmax=1.0,
            cmap="inferno",
            animated=False,
        )

        ax.set_title("Entanglement (DEBUG)")
        ax.set_xlabel("Qubit i")
        ax.set_ylabel("Qubit j")

    def update(self):
        sim = self.graph.simulation
        n = sim.num_qubits
        value = (self.graph.simulation.step_count % 100) / 100.0
        E = np.zeros((n, n))

        # 🔥 DEBUG SIGNAL — MORA SE MIJENJATI
        value = (sim.step_count % 100) / 100.0

        for i in range(n):
            E[i, i] = value

        self.im.set_data(E)
        self.im.autoscale()
