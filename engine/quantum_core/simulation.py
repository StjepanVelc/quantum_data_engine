import numpy as np
from engine.quantum_core.state_tools import custom_expm


class Simulation6Q:

    def __init__(self, register, hamiltonian, dt=0.1):
        self.reg = register
        self.H = hamiltonian.matrix
        self.dt = dt

        self.state = register.state.astype(complex)
        self.history = []
        self.num_qubits = 6

        self._record_state()

    # ---------------------------------------------------
    def step(self):
        U = custom_expm(-1j * self.H * self.dt)
        self.state = U @ self.state
        self.state = self.state / np.linalg.norm(self.state)
        self._record_state()

    # ---------------------------------------------------
    def _record_state(self):

        psi = self.state.reshape((64, 1))
        rho_full = psi @ psi.conj().T

        rho_qubits = []
        for q in range(6):
            rho_q = self._partial_trace(rho_full, q)
            rho_qubits.append(rho_q)

        self.history.append(
            {
                "state": self.state.copy(),
                "rho_full": rho_full,
                "rho_qubits": rho_qubits,
            }
        )

    # ---------------------------------------------------
    def _partial_trace(self, rho, target):
        """Tačan partial trace 64×64 → 2×2."""
        rho_out = np.zeros((2, 2), dtype=complex)

        for i in range(64):
            for j in range(64):

                bi = (i >> target) & 1
                bj = (j >> target) & 1

                if bi == bj:
                    rho_out[bi, bj] += rho[i, j]
                else:
                    rho_out[bi, bj] += rho[i, j]

        return rho_out
