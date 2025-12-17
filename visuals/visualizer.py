# visuals/visualizer.py
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from visuals.heatmap_view import HeatmapView
from visuals.graph_view import GraphView
from visuals.config import VisualizerConfig
from visuals.bloch_view import BlochView

_anim = None


def animate_graph(graph):
    # ==============================
    # FIGURE
    # ==============================
    global _anim
    fig = plt.figure(figsize=(16, 9))
    # ==============================
    # TITLE
    # ==============================
    ax_title = fig.add_axes([0.0, 0.92, 1.0, 0.06])
    ax_title.text(
        0.5,
        0.5,
        "Quantum Data Engine",
        ha="center",
        va="center",
        fontsize=16,
        weight="bold",
    )
    ax_title.axis("off")

    # ==============================
    # GRAPH VIEW
    # ==============================
    ax_graph = fig.add_axes([0.05, 0.08, 0.6, 0.82])
    graph_view = GraphView(ax_graph, graph)

    # ==============================
    # BLOCH VIEW (RIGHT PANEL)
    # ==============================
    bloch_view = None

    if VisualizerConfig.SHOW_BLOCH:
        bloch_axes = []
        cols, rows = 3, 2
        x0, y0 = 0.70, 0.55
        w, h = 0.25, 0.35
        dx, dy = w / cols, h / rows

        for r in range(rows):
            for c in range(cols):
                ax = fig.add_axes(
                    [x0 + c * dx, y0 + (rows - 1 - r) * dy, dx * 0.95, dy * 0.9]
                )
                bloch_axes.append(ax)

        bloch_view = BlochView(bloch_axes, graph)
        bloch_view.draw()

    # ==============================
    # HEATMAP VIEW (BOTTOM RIGHT)
    # ==============================
    heatmap_view = None

    if VisualizerConfig.SHOW_HEATMAP:
        ax_heat = fig.add_axes([0.70, 0.08, 0.25, 0.35])
        heatmap_view = HeatmapView(ax_heat, graph)

    # ==============================
    # UPDATE FUNCTION (SINGLE SOURCE OF TRUTH)
    # ==============================
    def update(frame):
        graph.simulation.step()
        t = frame / VisualizerConfig.FPS

        graph_view.update(t)

        if bloch_view and frame % VisualizerConfig.BLOCH_UPDATE_EVERY == 0:
            bloch_view.update()

        if heatmap_view and frame % VisualizerConfig.HEATMAP_UPDATE_EVERY == 0:
            heatmap_view.update()

        return []

    # ==============================
    # ANIMATION
    # ==============================
    _anim = FuncAnimation(
        fig,
        update,
        interval=1000 // VisualizerConfig.FPS,
        cache_frame_data=False,
        blit=False,
    )

    # --- FORCE proper fullscreen on Windows ---
    mng = plt.get_current_fig_manager()
    mng.window.state("zoomed")

    # ovo forsira da matplotlib ponovno izračuna layout
    plt.pause(0.1)
    mng.window.state("zoomed")

    plt.show()
    return _anim
