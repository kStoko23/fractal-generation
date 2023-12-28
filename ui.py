import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fractal_generation.mandelbrot_set import generate_mandelbrot
from fractal_generation.julia_set import generate_julia


class FractalApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Fractal Generator")
        self.geometry("800x600")

        self.default_zoom_factor = 1
        self.zoom_factor = self.default_zoom_factor
        self.default_center_x = 0
        self.center_x = self.default_center_x
        self.default_center_y = 0
        self.center_y = self.default_center_y
        self.default_xmin, self.default_xmax = -2, 1.5
        self.default_ymin, self.default_ymax = -2, 2

        self.colormap_choice = tk.StringVar(value="hot")

        self.canvas = None
        self.create_widgets()

    def create_widgets(self):
        self.sidebar = tk.Frame(self, width=200)
        self.sidebar.pack(fill=tk.Y, side=tk.LEFT, expand=False)

        self.display_area = tk.Label(self)
        self.display_area.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.add_settings()

    def add_settings(self):
        ttk.Label(self.sidebar, text="Liczba Iteracji:").pack()

        self.iteration_entry = ttk.Entry(self.sidebar)
        self.iteration_entry.insert(0, "100")
        self.iteration_entry.pack()

        self.fractal_choice = tk.StringVar(value="mandelbrot")
        fractals = [("Mandelbrot", "mandelbrot"), ("Julia", "julia")]
        ttk.Label(self.sidebar, text="Wybierz fraktal:").pack()
        for text, mode in fractals:
            ttk.Radiobutton(
                self.sidebar, text=text, variable=self.fractal_choice, value=mode
            ).pack()
        self.generate_button = ttk.Button(
            self.sidebar, text="Generuj", command=self.generate_fractal
        )
        self.generate_button.pack()
        self.reset_zoom_button = ttk.Button(
            self.sidebar, text="Reset Zoom", command=self.reset_zoom
        )
        self.reset_zoom_button.pack()
        ttk.Label(self.sidebar, text="Wybierz paletę kolorów:").pack()
        colormap_options = ["seismic", "hot", "pink", "hsv", "twilight_shifted"]
        colormap_menu = ttk.OptionMenu(
            self.sidebar,
            self.colormap_choice,
            self.colormap_choice.get(),
            *colormap_options
        )
        colormap_menu.pack()

    def reset_zoom(self):
        self.zoom_factor = self.default_zoom_factor
        self.center_x = self.default_center_x
        self.center_y = self.default_center_y
        self.xmin, self.xmax = self.default_xmin, self.default_xmax
        self.ymin, self.ymax = self.default_ymin, self.default_ymax
        self.generate_fractal()

    def clear_canvas(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

    def generate_fractal(self):
        self.clear_canvas()
        iterations = int(self.iteration_entry.get())
        chosen_fractal = self.fractal_choice.get()

        if chosen_fractal == "mandelbrot":
            fig = generate_mandelbrot(
                iterations=iterations,
                power=2,
                colormap=self.colormap_choice.get(),
                zoom_factor=self.zoom_factor,
                center_x=self.center_x,
                center_y=self.center_y,
            )
        elif chosen_fractal == "julia":
            julia_center = -0.05 - 0.66j
            fig = generate_julia(
                center=julia_center,
                interations=iterations,
                colormap=self.colormap_choice.get(),
                zoom_factor=self.zoom_factor,
                center_x=self.center_x,
                center_y=self.center_y,
            )
        self.canvas = FigureCanvasTkAgg(fig, master=self.display_area)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()
        self.canvas.mpl_connect("button_press_event", self.on_click)

    def on_click(self, event):
        if event.inaxes is not None:
            if event.button == 1:
                self.center_x, self.center_y = event.xdata, event.ydata
                self.zoom_factor /= 2
                self.generate_fractal()

            elif event.button == 3:
                self.center_x, self.center_y = event.xdata, event.ydata
                self.zoom_factor *= 2
                self.generate_fractal()

    def zoom_in(self):
        self.zoom_factor /= 2
        self.generate_fractal()

    def zoom_out(self):
        self.zoom_factor *= 2
        self.generate_fractal()


if __name__ == "__main__":
    app = FractalApp()
    app.mainloop()
