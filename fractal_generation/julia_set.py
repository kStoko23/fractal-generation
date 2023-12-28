import numpy as np
from matplotlib.figure import Figure


def generate_julia(
    center,
    interations,
    width=500,
    height=500,
    colormap="hot",
    zoom_factor=1,
    center_x=0,
    center_y=0,
):
    range_x = (3.5 * zoom_factor) / 2
    range_y = (4 * zoom_factor) / 2

    xDomain = np.linspace(center_x - range_x, center_x + range_x, width)
    yDomain = np.linspace(center_y - range_y, center_y + range_y, height)

    juliaSet = [[None for _ in xDomain] for _ in yDomain]

    for y in range(len(yDomain)):
        for x in range(len(xDomain)):
            z = complex(xDomain[x], yDomain[y])
            iteration = 0
            while abs(z) < 2 and iteration < interations:
                iteration += 1
                z = z**2 + center

            juliaSet[y][x] = iteration if iteration < interations else 0

    fig = Figure(figsize=(5, 4))
    ax = fig.add_subplot(111)
    ax.set_aspect("equal")
    plot = ax.pcolormesh(xDomain, yDomain, juliaSet, cmap=colormap)
    ax.set_xlabel("Real-Axis")
    ax.set_ylabel("Imaginary-Axis")
    title = f"Julia Set\nCenter = {center}, Zoom = {zoom_factor}, Max Iterations = {interations}"
    ax.set_title(title)
    fig.colorbar(plot)

    return fig
