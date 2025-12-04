import math
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate_graph(graph):

    # --- Build Graph Object ---
    G = nx.Graph()
    for node in graph.nodes:
        G.add_node(node.value, amplitude=node.amplitude, energy=node.energy)
        for linked in node.links:
            G.add_edge(node.value, linked.value)

    pos = nx.spring_layout(G, seed=42)

    # Color range
    amplitudes = [G.nodes[n]["amplitude"] for n in G.nodes]
    min_amp, max_amp = min(amplitudes), max(amplitudes)

    fig, ax = plt.subplots(figsize=(10, 7))

    # --- Colorbar ---
    sm = plt.cm.ScalarMappable(
        cmap=plt.cm.plasma, norm=plt.Normalize(vmin=min_amp, vmax=max_amp)
    )
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label("Amplitude")

    # Initial sizes & colors
    base_sizes = [G.nodes[n]["energy"] * 12 for n in G.nodes]
    base_colors = [node.amplitude for node in graph.nodes]

    # --- Nodes ---
    node_patch = nx.draw_networkx_nodes(
        G,
        pos,
        node_size=base_sizes,
        node_color=base_colors,
        cmap=plt.cm.plasma,
        ax=ax,
    )

    # --- Edges (but we store references) ---
    edge_lines = []
    for u, v in G.edges:
        line = ax.plot(
            [pos[u][0], pos[v][0]],
            [pos[u][1], pos[v][1]],
            color="gray",
            alpha=0.4,
            linewidth=2,
        )[0]
        edge_lines.append((u, v, line))

    # --- Labels (store references!) ---
    label_texts = {}
    for n in G.nodes:
        x, y = pos[n]
        lbl = ax.text(x, y, n, color="white", fontsize=12, ha="center", va="center")
        label_texts[n] = lbl

    ax.set_title("Quantum Graph Visualization (Animated)")
    ax.set_axis_off()

    # ------------------------------------------------------
    # UPDATE FRAME
    # ------------------------------------------------------
    def update(frame):
        t = frame / 5.0

        drifted_pos = {}

        # --- Node amplitude pulsing ---
        new_colors = []
        new_sizes = []

        for i, node in enumerate(graph.nodes):
            # amplitude oscillation
            pulse = 0.25 * math.sin(t + node.energy / 50)
            amp = max(0.05, min(1.0, node.amplitude + pulse))
            new_colors.append(amp)

            # size oscillation
            base_size = node.energy * 12
            new_sizes.append(base_size * (1 + 0.1 * math.sin(t)))

        node_patch.set_array(new_colors)
        node_patch.set_sizes(new_sizes)

        # --- Node positional drift ---
        for i, n in enumerate(G.nodes):
            x, y = pos[n]
            dx = 0.02 * math.sin(t + i)
            dy = 0.02 * math.cos(t + i * 1.2)
            drifted_pos[n] = (x + dx, y + dy)

        # Apply new node positions
        node_patch.set_offsets([drifted_pos[n] for n in G.nodes])

        # --- Update edge line coordinates ---
        for u, v, line in edge_lines:
            x1, y1 = drifted_pos[u]
            x2, y2 = drifted_pos[v]
            line.set_xdata([x1, x2])
            line.set_ydata([y1, y2])

        # --- Update label positions ---
        for n in G.nodes:
            x, y = drifted_pos[n]
            label_texts[n].set_position((x, y))

        return (node_patch,)

    # ------------------------------------------------------

    anim = FuncAnimation(fig, update, frames=200, interval=60, blit=False)
    plt.show()
