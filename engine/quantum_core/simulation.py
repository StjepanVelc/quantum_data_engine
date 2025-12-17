import numpy as np
from engine.quantum_core.state_tools import custom_expm, partial_trace_single
from engine.quantum_core.quantum_gates import X
from engine.quantum_core.quantum_gates import U3
from engine.quantum_core.state_tools import von_neumann_entropy


class Simulation6Q:
    def __init__(self, register, hamiltonian, dt=0.1):
        self.reg = register
        self.register = register

        self.hamiltonian = hamiltonian
        self.H = hamiltonian.matrix

        self.dt = dt
        self.step_count = 0
        self.state = register.state.astype(complex)
        self.history = []
        self.num_qubits = register.num_qubits
        self._record_state()

        self.register = register

    # --------------------------------------------------
    def step(self):
        self.step_count += 1
        t = self.step_count * self.dt

        # total Hamiltonian = static + drive
        H_total = self.H + self.hamiltonian.drive_term(t)

        U = custom_expm(-1j * H_total * self.dt)

        self.state = U @ self.state
        self.state /= np.linalg.norm(self.state)

        self.reg.set_state(self.state)
        self._record_state()

    # --------------------------------------------------
    def _record_state(self):
        rho_qubits = [partial_trace_single(self.state, q) for q in range(6)]

        entropy = [von_neumann_entropy(rho) for rho in rho_qubits]

        # opcionalno: izloži trenutno stanje registra (za C# / UI)
        self.reg.entropies = entropy

        self.history.append(
            {
                "state": self.state.copy(),
                "rho_qubits": rho_qubits,
                "entropy": entropy,
            }
        )
