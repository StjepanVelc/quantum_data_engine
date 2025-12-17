import math
import networkx as nx
import matplotlib.pyplot as plt


class GraphView:
    def __init__(self, ax, quantum_graph):
        self.ax = ax
        self.graph = quantum_graph
        self.G = nx.Graph()

        self._build_graph()
        self._draw_static()

    def _build_graph(self):
        for node in self.graph.nodes:
            self.G.add_node(node.value, amplitude=node.amplitude, energy=node.energy)
            for link in node.links:
                self.G.add_edge(node.value, link.value)

        self.pos = nx.spring_layout(self.G, seed=42)

    def _draw_static(self):
        amplitudes = [self.G.nodes[n]["amplitude"] for n in self.G.nodes]
        sizes = [self.G.nodes[n]["energy"] * 12 for n in self.G.nodes]

        self.nodes_artist = nx.draw_networkx_nodes(
            self.G,
            self.pos,
            node_color=amplitudes,
            node_size=sizes,
            cmap=plt.cm.plasma,
            ax=self.ax,
        )

        self.edge_artists = []
        for u, v in self.G.edges:
            line = self.ax.plot(
                [self.pos[u][0], self.pos[v][0]],
                [self.pos[u][1], self.pos[v][1]],
                color="gray",
                alpha=0.4,
            )[0]
            self.edge_artists.append((u, v, line))

        self.labels = {
            n: self.ax.text(*self.pos[n], n, color="white") for n in self.G.nodes
        }

        self.ax.set_title("Quantum Network")
        self.ax.set_axis_off()

    def update(self, t):
        new_colors = []
        new_sizes = {}
        drifted = {}

        for i, node in enumerate(self.graph.nodes):
            pulse = 0.25 * math.sin(t + node.energy / 50)
            amp = max(0.05, min(1.0, node.amplitude + pulse))
            new_colors.append(amp)
            new_sizes[node.value] = node.energy * 12

        self.nodes_artist.set_array(new_colors)
        self.nodes_artist.set_sizes(list(new_sizes.values()))

        for i, n in enumerate(self.G.nodes):
            x, y = self.pos[n]
            drifted[n] = (x + 0.01 * math.sin(t + i), y + 0.01 * math.cos(t + i))

        self.nodes_artist.set_offsets([drifted[n] for n in self.G.nodes])

        for u, v, line in self.edge_artists:
            x1, y1 = drifted[u]
            x2, y2 = drifted[v]
            line.set_xdata([x1, x2])
            line.set_ydata([y1, y2])

        for n in self.labels:
            self.labels[n].set_position(drifted[n])
