"""Embed a matplotlib trend chart inside a tkinter frame."""

from datetime import datetime
import matplotlib
matplotlib.use("TkAgg")  # must be set before importing pyplot

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def build_trend_canvas(parent, history):
    """
    history: list of (recorded_at_iso_string, bmi)
    Returns a tkinter widget containing the chart.
    """
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)

    if not history:
        ax.text(0.5, 0.5, "No records yet",
                ha="center", va="center", fontsize=12, color="gray")
        ax.set_axis_off()
    else:
        dates = [datetime.fromisoformat(ts).strftime("%b %d %H:%M") for ts, _ in history]
        bmis = [b for _, b in history]
        ax.plot(dates, bmis, marker="o", color="#2ecc71", linewidth=2)
        ax.set_ylabel("BMI")
        ax.set_title("BMI Trend")
        ax.tick_params(axis="x", rotation=45, labelsize=8)
        ax.grid(alpha=0.3)

    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    return canvas.get_tk_widget()