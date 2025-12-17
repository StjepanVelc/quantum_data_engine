import numpy as np
import matplotlib.pyplot as plt
from engine.quantum_core.state_tools import partial_trace_single


class BlochView:
    def __init__(self, axes, graph):
        self.axes = axes
        self.graph = graph
        self.lines = []

    def draw(self):
        self.lines.clear()

        for ax in self.axes:
            ax.clear()
            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            ax.set_aspect("equal")
            ax.axis("off")

            # Bloch circle
            ax.add_patch(plt.Circle((0, 0), 0.9, fill=False, alpha=0.3))

            # Bloch vector as LINE (not arrow)
            (line,) = ax.plot([0, 0], [0, 0.8], color="red", lw=2)
            self.lines.append(line)

    def update(self):
        reg = self.graph.simulation.register

        for i, line in enumerate(self.lines):
            if i >= reg.n:
                line.set_visible(False)
                continue

            x, y, z = self._bloch_from_state(reg, i)

            # project Bloch sphere: X-Z plane
            line.set_data([0, x], [0, z])
            line.set_visible(True)

    # --------------------------------------------------

    def _bloch_from_state(self, reg, qubit):
        rho = partial_trace_single(reg.state, qubit, reg.num_qubits)

        sx = np.array([[0, 1], [1, 0]], dtype=complex)
        sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
        sz = np.array([[1, 0], [0, -1]], dtype=complex)

        return (
            np.real(np.trace(rho @ sx)),
            np.real(np.trace(rho @ sy)),
            np.real(np.trace(rho @ sz)),
        )
