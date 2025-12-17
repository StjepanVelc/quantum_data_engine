import numpy as np


# ---------------------------------------------------------
# Bloch vector
# ---------------------------------------------------------
def bloch_vector(rho):
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.array([[1, 0], [0, -1]])

    return np.array(
        [
            np.real(np.trace(rho @ X)),
            np.real(np.trace(rho @ Y)),
            np.real(np.trace(rho @ Z)),
        ]
    )


# ---------------------------------------------------------
# Matrix exponential (bez SciPy)
# ---------------------------------------------------------
def custom_expm(A):
    n = 8
    A_scaled = A / (2**n)

    X = np.eye(A.shape[0], dtype=complex)
    term = np.eye(A.shape[0], dtype=complex)

    for k in range(1, 40):
        term = term @ (A_scaled / k)
        X += term

    for _ in range(n):
        X = X @ X

    return X


# ---------------------------------------------------------
# PARTIAL TRACE (6 qubita → 1 qubit)
# ---------------------------------------------------------
def partial_trace_single(state, target, num_qubits=6):
    """
    state: globalni state vektor (64,)
    target: koji qubit (0–5)
    return: 2x2 density matrix
    """
    psi = state.reshape([2] * num_qubits)

    rho = np.tensordot(
        psi,
        np.conj(psi),
        axes=(
            [i for i in range(num_qubits) if i != target],
            [i for i in range(num_qubits) if i != target],
        ),
    )

    return rho

import numpy as np


def von_neumann_entropy(rho, eps=1e-12):
    """
    Entanglement entropy S = -Tr(rho log2 rho)
    rho: 2x2 density matrix
    """
    # eigenvalues
    vals = np.linalg.eigvalsh(rho)

    # numerical safety
    vals = np.clip(vals, eps, 1.0)

    return -np.sum(vals * np.log2(vals))
