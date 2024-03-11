import tkinter as tk
from tkinter import ttk

class create_app():
    def __init__(self,
                 generator_function,
                 point_size: int = 3,
                 canvas_size: int = 600,) -> None:
        self.generator_function = generator_function
        self.point_size = point_size
        self.canvas_size = canvas_size
    
    def setup_gui(self):
        # Create the main window
        self.root_ = tk.Tk()
        self.root_.title("Pi Estimation using Monte Carlo Simulation")

        # Create a frame for the controls
        frame = ttk.Frame(self.root_, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Entry for the number of points
        self.points_entry_ = ttk.Entry(frame, width=10)
        self.points_entry_.grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Label(frame, text="Number of Points:").grid(row=0, column=0, sticky=tk.W)

        # Start button
        start_button = ttk.Button(frame, text="Start", command=self.start_simulation)
        start_button.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # Label for showing the result
        self.result_label_ = ttk.Label(self.root_, text="Pi Estimate:")
        self.result_label_.grid(row=2, column=0, sticky=(tk.W, tk.E))

        # Canvas for drawing the points
        self.drawing_canvas_ = tk.Canvas(self.root_, width=self.canvas_size,
                                         height=self.canvas_size, background="white")
        self.drawing_canvas_.create_arc(-self.canvas_size, -self.canvas_size,
                                        self.canvas_size, self.canvas_size,
                                        start=0, extent=-90, style=tk.ARC, outline='blue')
        self.drawing_canvas_.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def simulate_pi_partially(self, generator):
        try:
            point_info, inside_count, total_points = next(generator)
            (x, y, inside) = point_info
            pi_estimate = 4 * inside_count / total_points
            color = 'red' if inside else 'green'
            self.drawing_canvas_.create_oval(x * self.canvas_size,
                                             y * self.canvas_size,
                                             x * self.canvas_size + self.point_size,
                                             y * self.canvas_size + self.point_size,
                                             fill=color, outline=color)
            self.result_label_.config(text=f"Pi Estimate: {pi_estimate:.10f}")
            self.drawing_canvas_.after(1, self.simulate_pi_partially,
                                       generator)
        except StopIteration:
            pass

    def start_simulation(self):
        n_samples = int(self.points_entry_.get())
        generator = self.generator_function(n_samples)
        self.drawing_canvas_.delete('all')
        self.drawing_canvas_.create_arc(-self.canvas_size, -self.canvas_size,
                                        self.canvas_size, self.canvas_size,
                                        start=0, extent=-90, style=tk.ARC, outline='blue')
        self.simulate_pi_partially(generator)

    def run(self):
        self.root_.mainloop()


