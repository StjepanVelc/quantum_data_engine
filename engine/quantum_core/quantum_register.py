import numpy as np


class QuantumRegister:
    """
    6-qubit kvantni registar koji upravlja globalnim 64-dimenzionalnim stanjem.
    """

    def __init__(self, num_qubits=6):
        self.num_qubits = num_qubits
        self.dim = 2**num_qubits

        # --- Random normalized initial state ---
        psi = np.random.randn(self.dim) + 1j * np.random.randn(self.dim)
        self.state = psi / np.linalg.norm(psi)

    # --------------------------------------------------------
    # STANJE
    # --------------------------------------------------------

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state / np.linalg.norm(new_state)

    # --------------------------------------------------------
    # APPLY SINGLE-QUBIT GATE
    # --------------------------------------------------------

    def apply_gate(self, gate_matrix, qubit_index):
        """
        gate_matrix = 2x2 gate (X, Y, Z, H, S, T, U3...)
        qubit_index = 0–5
        """
        I = np.eye(2)
        ops = []

        for i in range(self.num_qubits):
            ops.append(gate_matrix if i == qubit_index else I)

        full_op = ops[0]
        for i in range(1, self.num_qubits):
            full_op = np.kron(full_op, ops[i])

        self.state = full_op @ self.state

    # --------------------------------------------------------
    # CONTROLLED GATE (CNOT / CU)
    # --------------------------------------------------------

    def apply_controlled(self, control, target, gate):
        """
        control = qubit index
        target = qubit index
        gate = 2x2 matrix (X, Y, Z, H, U3...)
        """
        I = np.eye(2)
        P0 = np.array([[1, 0], [0, 0]])
        P1 = np.array([[0, 0], [0, 1]])

        ops_zero = []
        ops_one = []

        for i in range(self.num_qubits):
            if i == control:
                ops_zero.append(P0)
                ops_one.append(P1)
            elif i == target:
                ops_zero.append(I)
                ops_one.append(gate)
            else:
                ops_zero.append(I)
                ops_one.append(I)

        # Kronecker build
        M0 = ops_zero[0]
        M1 = ops_one[0]
        for i in range(1, self.num_qubits):
            M0 = np.kron(M0, ops_zero[i])
            M1 = np.kron(M1, ops_one[i])

        U = M0 + M1
        self.state = U @ self.state

    # --------------------------------------------------------
    # RETURN REDUCED SINGLE-QUBIT DENSITY MATRIX
    # --------------------------------------------------------

    def reduced_density_matrix(self, qubit_index):
        """
        Partial trace nad svim ostalim qubitima — dobije se 2×2 matrica.
        """

        psi = self.state.reshape([2] * self.num_qubits)
        rho = np.tensordot(
            psi,
            np.conj(psi),
            axes=(
                [i for i in range(self.num_qubits) if i != qubit_index],
                [i for i in range(self.num_qubits) if i != qubit_index],
            ),
        )
        return rho
