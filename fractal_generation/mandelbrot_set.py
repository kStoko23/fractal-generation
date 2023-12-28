import numpy as np
from matplotlib.figure import Figure


def generate_mandelbrot(
    iterations,
    width=500,
    height=500,
    power=2,
    colormap="hot",
    zoom_factor=1,
    center_x=0,
    center_y=0,
):
    range_x = (3.5 * zoom_factor) / 2
    range_y = (4 * zoom_factor) / 2

    xDomain = np.linspace(center_x - range_x, center_x + range_x, width)
    yDomain = np.linspace(center_y - range_y, center_y + range_y, height)

    bound = 2
    iterationArray = []

    for y in yDomain:
        row = []
        for x in xDomain:
            c = complex(x, y)
            z = 0
            for iterationNumber in range(iterations):
                if abs(z) >= bound:
                    row.append(iterationNumber)
                    break
                else:
                    z = z**power + c
            else:
                row.append(0)
        iterationArray.append(row)

    fig = Figure(figsize=(5, 4))
    ax = fig.add_subplot(111)
    ax.set_aspect("equal")
    ax.pcolormesh(xDomain, yDomain, iterationArray, cmap=colormap)
    ax.set_xlabel("Real-Axis")
    ax.set_ylabel("Imaginary-Axis")
    title = f"Multibrot set for $z_{{new}} = z^{{{power}}} + c$ with {iterations} iterations, zoom {zoom_factor}"
    ax.set_title(title)

    return fig
