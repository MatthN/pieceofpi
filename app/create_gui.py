import tkinter as tk
from tkinter import ttk
from typing import Generator, Tuple

class create_app():
    def __init__(self,
                 generator_function: Generator[Tuple[Tuple[float, float, int],
                                                     int, int], None, None],
                 point_size: int = 3,
                 canvas_size: int = 600,
                 smoothing_window_size: int = 50) -> None:
        self.generator_function = generator_function
        self.point_size = point_size
        self.canvas_size = canvas_size
        self.paused_ = False
        self.pi_values_ = []
        self.smoothing_window_size = smoothing_window_size
    
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

        # Pause/Resume button
        self.pause_button_ = ttk.Button(frame, text="Pause", command=self.toggle_pause)
        self.pause_button_.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # Label for showing the result
        self.result_label_ = ttk.Label(self.root_, text="Pi Estimate:")
        self.result_label_.grid(row=2, column=0, sticky=(tk.W, tk.E))

        # Label for showing the points counter
        self.points_counter_label_ = ttk.Label(self.root_, text="Points: 0")
        self.points_counter_label_.grid(row=4, column=0, sticky=(tk.W, tk.E))

        # Canvas for drawing the points
        self.drawing_canvas_ = tk.Canvas(self.root_, width=self.canvas_size,
                                         height=self.canvas_size, background="white")
        self.drawing_canvas_.create_arc(-self.canvas_size, -self.canvas_size,
                                        self.canvas_size, self.canvas_size,
                                        start=0, extent=-90, style=tk.ARC, outline='blue')
        self.drawing_canvas_.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def toggle_pause(self):
        self.paused_ = not self.paused_
        self.pause_button_.config(text="Resume" if self.paused_ else "Pause")
    
    def smooth_pi_estimate(self, pi_estimate):
        self.pi_values_.append(pi_estimate)
        if len(self.pi_values_) > self.smoothing_window_size:
            self.pi_values_.pop(0)
        
        smoothed_pi = sum(self.pi_values_) / len(self.pi_values_)
        return smoothed_pi

    def simulate_pi_partially(self, generator):
        if self.paused_:
            # If paused, wait for a bit and then check again
            self.drawing_canvas_.after(100, self.simulate_pi_partially, generator)
        else:
            try:
                point_info, inside_count, total_points = next(generator)
                (x, y, inside) = point_info
                pi_estimate = 4 * inside_count / total_points
                smoothed_pi = self.smooth_pi_estimate(pi_estimate)
                color = 'red' if inside else 'green'
                self.drawing_canvas_.create_oval(x * self.canvas_size,
                                                y * self.canvas_size,
                                                x * self.canvas_size + self.point_size,
                                                y * self.canvas_size + self.point_size,
                                                fill=color, outline=color)
                self.result_label_.config(text=f"Pi Estimate: {smoothed_pi:.10f}")
                self.points_counter_label_.config(text=f"Points: {total_points}")
                self.drawing_canvas_.after(1, self.simulate_pi_partially,
                                        generator)
            except StopIteration:
                pass

    def start_simulation(self):
        self.drawing_canvas_.delete('all')
        self.drawing_canvas_.create_arc(-self.canvas_size, -self.canvas_size,
                                        self.canvas_size, self.canvas_size,
                                        start=0, extent=-90, style=tk.ARC, outline='blue')
        self.paused_ = False  # Reset pause state when simulation starts
        self.pause_button_.config(text="Pause")  # Reset button text to "Pause"
        n_samples = int(self.points_entry_.get())
        generator = self.generator_function(n_samples)
        self.simulate_pi_partially(generator)

    def run(self):
        self.root_.mainloop()


