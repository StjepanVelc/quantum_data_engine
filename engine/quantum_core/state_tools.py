import numpy as np


# ---------------------------------------------------------
# Bloch vector
# ---------------------------------------------------------
def bloch_vector(rho):

    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.array([[1, 0], [0, -1]])

    bx = np.real(np.trace(rho @ X))
    by = np.real(np.trace(rho @ Y))
    bz = np.real(np.trace(rho @ Z))

    return np.array([bx, by, bz])


# ---------------------------------------------------------
# custom expm (bez SciPy)
# ---------------------------------------------------------
def custom_expm(A):
    """Matrix exponential — scaling & squaring."""
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
