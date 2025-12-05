import numpy as np


class Hamiltonian6Q:
    """
    Ising Hamiltonian za 6 qubita u linearnom lancu.
    H = J Σ σ_z(i) σ_z(i+1) + h Σ σ_x(i)
    """

    def __init__(self, J=1.0, h=0.7):
        self.J = J
        self.h = h
        self.I = np.eye(2)
        self.Z = np.array([[1, 0], [0, -1]])
        self.X = np.array([[0, 1], [1, 0]])
        self.num_qubits = 6
        self.dim = 64

        self.matrix = self.build_hamiltonian()

    # ----------------------------------------------------------

    def kron_n(self, ops):
        M = ops[0]
        for i in range(1, len(ops)):
            M = np.kron(M, ops[i])
        return M

    # ----------------------------------------------------------

    def build_hamiltonian(self):
        H = np.zeros((self.dim, self.dim), dtype=complex)

        # --- Interaction terms ---
        for i in range(5):  # Q0-Q1, Q1-Q2, ..., Q4-Q5
            ops = []
            for pos in range(6):
                if pos == i or pos == i + 1:
                    ops.append(self.Z)
                else:
                    ops.append(self.I)
            H += self.J * self.kron_n(ops)

        # --- Transverse field ---
        for i in range(6):
            ops = []
            for pos in range(6):
                ops.append(self.X if pos == i else self.I)
            H += self.h * self.kron_n(ops)

        return H
