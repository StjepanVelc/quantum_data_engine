import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from engine.quantum_core.state_tools import bloch_vector


# =========================================================
#   BLOCH SPHERE HELPERS
# =========================================================


def draw_bloch_sphere(ax):
    ax.clear()

    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 25)

    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))

    ax.plot_surface(
        x,
        y,
        z,
        rstride=1,
        cstride=1,
        color="cyan",
        alpha=0.10,
        edgecolor="white",
        linewidth=0.2,
    )

    ax.quiver(0, 0, 0, 1, 0, 0, color="red")
    ax.quiver(0, 0, 0, 0, 1, 0, color="green")
    ax.quiver(0, 0, 0, 0, 0, 1, color="blue")

    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_box_aspect([1, 1, 1])
    ax.axis("off")


def draw_bloch_vector(ax, bloch):
    bx, by, bz = bloch
    ax.quiver(0, 0, 0, bx, by, bz, color="yellow", linewidth=3)


# =========================================================
#   HEATMAP
# =========================================================


def get_interference(sim):
    """64×64 density matrix → 8×8 heatmap by block averaging."""
    if len(sim.history) == 0:
        return np.zeros((8, 8))

    rho = sim.history[-1]["rho_full"]

    # uzmemo realni dio, magnituda
    M = np.abs(np.real(rho))

    # blokovi 8×8 → 8x8 izlaz
    out = np.zeros((8, 8))

    for i in range(8):  # rows
        for j in range(8):  # cols
            block = M[i * 8 : (i + 1) * 8, j * 8 : (j + 1) * 8]
            out[i, j] = block.mean()  # prosjek bloka

    return out


# =========================================================
#   MAIN VISUALIZER
# =========================================================


def animate_graph(graph):

    fig = plt.figure(figsize=(16, 9))

    ax_graph = fig.add_axes([0.05, 0.05, 0.56, 0.90])
    ax_sidebar = fig.add_axes([0.64, 0.60, 0.31, 0.35])
    ax_sidebar.axis("off")
    ax_heat = fig.add_axes([0.70, 0.05, 0.25, 0.35])

    # -----------------------------------------------------
    # GRAPH NETWORK
    # -----------------------------------------------------
    G = nx.Graph()
    for node in graph.nodes:
        G.add_node(node.value, amplitude=node.amplitude, energy=node.energy)
        for linked in node.links:
            G.add_edge(node.value, linked.value)

    pos = nx.spring_layout(G, seed=42)

    amps = [G.nodes[n]["amplitude"] for n in G.nodes]
    sizes = [G.nodes[n]["energy"] * 12 for n in G.nodes]

    node_patch = nx.draw_networkx_nodes(
        G, pos, node_size=sizes, node_color=amps, cmap=plt.cm.plasma, ax=ax_graph
    )

    # edges
    edge_lines = []
    for u, v in G.edges:
        line = ax_graph.plot(
            [pos[u][0], pos[v][0]],
            [pos[u][1], pos[v][1]],
            color="gray",
            alpha=0.4,
            linewidth=2,
        )[0]
        edge_lines.append((u, v, line))

    label_texts = {}
    for n in G.nodes:
        (x, y) = pos[n]
        label_texts[n] = ax_graph.text(x, y, n, color="white")

    ax_graph.set_title("Quantum Network Visualization (6Q Engine)")
    ax_graph.set_axis_off()

    # -----------------------------------------------------
    # BLOCH SPHERES
    # -----------------------------------------------------
    qubits = graph.quantum_nodes[:6]

    grid = [
        (0.64, 0.55),
        (0.76, 0.55),
        (0.88, 0.55),
        (0.64, 0.35),
        (0.76, 0.35),
        (0.88, 0.35),
    ]

    bloch_axes = []
    for i, node in enumerate(qubits):
        ax = fig.add_axes([grid[i][0], grid[i][1], 0.12, 0.18], projection="3d")
        draw_bloch_sphere(ax)
        bloch_axes.append(ax)

    # -----------------------------------------------------
    # HEATMAP INITIAL
    # -----------------------------------------------------
    heat_img = ax_heat.imshow(get_interference(graph.simulation), cmap="inferno")
    ax_heat.set_title("Interference Heatmap")

    # -----------------------------------------------------
    # UPDATE FUNCTION
    # -----------------------------------------------------

    def update(frame):

        t = frame / 6.0
        drifted = {}

        new_colors = []
        new_sizes = []

        # Node amplitude pulse + drift
        for i, node in enumerate(graph.nodes):
            pulse = 0.25 * math.sin(t + node.energy / 50)
            amp = max(0.05, min(1.0, node.amplitude + pulse))

            new_colors.append(amp)
            new_sizes.append(node.energy * 12 * (1 + 0.15 * math.sin(t)))

        node_patch.set_array(new_colors)
        node_patch.set_sizes(new_sizes)

        # Node drifting
        for i, n in enumerate(G.nodes):
            (x, y) = pos[n]
            dx = 0.02 * math.sin(t + 0.3 * i)
            dy = 0.02 * math.cos(t + 0.5 * i)
            drifted[n] = (x + dx, y + dy)

        node_patch.set_offsets([drifted[n] for n in G.nodes])

        # Update edges
        for u, v, line in edge_lines:
            (x1, y1) = drifted[u]
            (x2, y2) = drifted[v]
            line.set_xdata([x1, x2])
            line.set_ydata([y1, y2])

        # Update labels
        for n in G.nodes:
            (x, y) = drifted[n]
            label_texts[n].set_position((x, y))

        # Quantum simulation step
        graph.simulation.step()
        frame_data = graph.simulation.history[-1]

        # Update Bloch spheres
        for node, ax in zip(qubits, bloch_axes):
            draw_bloch_sphere(ax)
            rho = frame_data["rho_qubits"][node.qubit_index]
            bloch = bloch_vector(rho)
            draw_bloch_vector(ax, bloch)

        # Update heatmap
        heat_img.set_data(get_interference(graph.simulation))

        # Sidebar info
        ax_sidebar.clear()
        ax_sidebar.axis("off")

        txt = "QUANTUM STATE\n\n"
        for node in qubits:
            txt += f"Q{node.qubit_index} ({node.value})\n"
            txt += f" Amp = {node.amplitude:.2f}\n"
            txt += f" Energy = {node.energy:.1f}\n\n"

        ax_sidebar.text(0.0, 1.0, txt, color="white", va="top")

        # 🔥 MUST RETURN ALL ARTISTS SO ANIMATION UPDATES
        return [node_patch, heat_img] + bloch_axes

    # -----------------------------------------------------
    # START ANIMATION
    # -----------------------------------------------------
    anim = FuncAnimation(fig, update, frames=500, interval=60, blit=False)
    plt.show()
