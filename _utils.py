import sys

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider


def get_samples():
    samples = sorted(np.load("samples.npy").tolist(), key=lambda x: x[0])
    return [(x[0], x[1]) for x in samples]


def plot_live_ecg(live_ecg, samples, plot_width):
    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots()
    line, = ax.plot(0, 0)
    ax.set_ylim(-300, 500)
    ax.set_xlim(0, plot_width)
    ax.set_xlabel('Time [ns]')

    min_ts = samples[0][0]
    max_ts = min_ts + 4 * plot_width

    # adjust the main plot to make room for the sliders
    fig.subplots_adjust(left=0.25, bottom=0.25)

    slider_ax = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    slider = Slider(
        ax=slider_ax,
        label='Progress',
        valmin=min_ts,
        valmax=max_ts + plot_width,
        valinit=min_ts,
    )

    # The function to be called anytime a slider's value changes
    def update(val):
        to_display = live_ecg.display_slice(val)
        if len(to_display) == 0:
            print("Empty list passed at timestamp", int(val), file=sys.stderr)
        else:
            # insert a None value to disconnect the halfs of the plot if it is non-chronological
            to_display.append((to_display[-1][0], None))
            to_display.sort(key=lambda x: x[0])
            line.set_data(*list(zip(*to_display)))
        fig.canvas.draw_idle()

    # register the update function with each slider
    slider.on_changed(update)

    update(min_ts)

    plt.show()
