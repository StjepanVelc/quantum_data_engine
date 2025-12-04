from engine.node import QuantumNode
from engine.graph import QuantumGraph
from storage.search_engine import SearchEngine

from engine.quantum_ops import QuantumOps
from visuals.visualizer import animate_graph

print("Quantum Data Engine running...")

# ---------------------------------------
# 1) Građenje grafa
# ---------------------------------------
g = QuantumGraph()

a = QuantumNode("A", energy=50)
b = QuantumNode("B", energy=10)
c = QuantumNode("C", energy=90)

# Set amplitude
a.amplitude = 0.40
b.amplitude = 0.10
c.amplitude = 0.85

# Dodavanje u graf
g.add_node(a)
g.add_node(b)
g.add_node(c)

# Spajanje čvorova
g.connect(a, b)
g.connect(a, c)

# Prikaz linkova
print("A links:", a.links)
print("B links:", b.links)
print("C links:", c.links)

# ---------------------------------------
# 2) SearchEngine demo
# ---------------------------------------
engine = SearchEngine()
engine.rebuild(g.nodes)

print("\n--- SEARCH TESTS ---")
print("Amplitude > 0.3:", engine.by_amplitude(0.3))
print("Energy > 20:", engine.by_energy(20))
print("Find value 'B':", engine.by_value("B"))
print("Combined filter:", engine.combined(min_amp=0.3, min_energy=40))
print("Ranked:", engine.ranked(min_amp=0.1, min_energy=5))

# ---------------------------------------
# 3) ENTANGLEMENT TEST (X & Y)
# ---------------------------------------
print("\n--- ENTANGLEMENT TEST ---")

x = QuantumNode("X", amplitude=0.8, energy=60)
y = QuantumNode("Y", amplitude=0.2, energy=40)

QuantumOps.entangle(x, y)
print("Spregnuti su:", x.entangled_with)

result = QuantumOps.collapse(x)
print("X collapsed to:", result)
print("X amplitude:", x.amplitude)
print("Y amplitude:", y.amplitude)

# Ako želiš vizualni prikaz entanglementa — dodaj ih u graf:
g.add_node(x)
g.add_node(y)
g.connect(x, y)

print("\nRendering graph...")
animate_graph(g)
