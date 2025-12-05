import numpy as np

from engine.node import QuantumNode
from engine.graph import QuantumGraph
from storage.search_engine import SearchEngine

from visuals.visualizer import animate_graph

# Quantum Core
from engine.quantum_core.quantum_register import QuantumRegister
from engine.quantum_core.hamiltonian import Hamiltonian6Q
from engine.quantum_core.simulation import Simulation6Q
from engine.quantum_core import quantum_gates as G

print("\nQuantum Data Engine — 6Q MODE\n")


# =========================================================
# 1) Build Graph Nodes
# =========================================================
g = QuantumGraph()

nodes = [
    QuantumNode("A", amplitude=0.3, energy=30),
    QuantumNode("B", amplitude=0.5, energy=50),
    QuantumNode("C", amplitude=0.8, energy=70),
    QuantumNode("D", amplitude=0.6, energy=40),
    QuantumNode("E", amplitude=0.9, energy=90),
    QuantumNode("F", amplitude=0.4, energy=20),
]

for n in nodes:
    g.add_node(n)

for i, n in enumerate(nodes):
    n.qubit_index = i

# linear chain connectivity
g.connect(nodes[0], nodes[1])
g.connect(nodes[1], nodes[2])
g.connect(nodes[2], nodes[3])
g.connect(nodes[3], nodes[4])
g.connect(nodes[4], nodes[5])

print("Graph constructed.")


# =========================================================
# 2) 6-Qubit Quantum Register
# =========================================================
reg = QuantumRegister(6)

# označimo čvorove kao qubite radi vizualizacije
for n in nodes:
    n.is_qubit = True

# vizualizator treba listu qubit-nodes
g.quantum_nodes = nodes


# =========================================================
# 3) APPLY QUANTUM GATES (Samo kompatibilni!)
# =========================================================

# H on qubit 0
reg.apply_gate(G.H, 0)

# X on qubit 3
reg.apply_gate(G.X, 3)

# Z on qubit 5
reg.apply_gate(G.Z, 5)

# phase rotation using phase(theta)
reg.apply_gate(G.phase(0.4), 1)

# U3 arbitrary rotation
reg.apply_gate(G.U3(0.8, 0.3, 0.5), 2)

# S and T gates
reg.apply_gate(G.S, 4)
reg.apply_gate(G.T, 0)

print("Quantum gates applied.")

# =========================================================
# 4) Hamiltonian + Simulation
# =========================================================
H = Hamiltonian6Q(J=1.0, h=0.7)

sim = Simulation6Q(reg, H, dt=0.1)

# vizualizator očekuje ovo!
g.simulation = sim

# =========================================================
# 5) Visualization
# =========================================================
print("Launching visualization…")
animate_graph(g)
