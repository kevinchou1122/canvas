from tkinter import *
from tkinter import colorchooser
import math


# noinspection PyArgumentList
class ArtCanvas(Frame):
    def __init__(self, master):
        """Initialize the ArtCanvas frame."""
        Frame.__init__(self, master)
        self.grid()

        # Create the left control panel
        self.left_section = Frame(self, width=150, height=50, bg="lightgrey")
        self.left_section.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        self.left_section.grid_propagate(False)

        # Create the Canvas for drawing
        self.canvas = Canvas(self, width=1000, height=850, bg="white")
        self.canvas.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Slider and update button for line thickness
        self.slider = Scale(self.left_section, from_=1, to=10, orient=HORIZONTAL, label="Line Thickness")
        self.slider.grid(row=0, column=0, padx=5, pady=5)
        self.slider.bind("<Motion>", self.update_thickness)

        self.color_button = Button(self.left_section, text="Choose Color", command=self.choose_color)
        self.color_button.grid(row=1, column=0, padx=5, pady=5)

        self.erase_button= Button(self.left_section, text="Eraser", command=self.erase)
        self.erase_button.grid(row=3, column=0, padx=5, pady=5)
        self.clear_button=Button(self.left_section, text="Clear Screen", command=self.clear_canvas)
        self.clear_button.grid(row=4, column=0, padx=5, pady=5)


        # Initialize the color with a default value
        self.selected_color = "black"

        # Bind mouse events for drawing
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<Button-2>", self.draw_dot)
        self.canvas.bind("<B1-Motion>", self.track_mouse)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)


        # Initialize variables
        self.line_thickness = 5
        self.radius=5
        self.points = []  # Store points for smoothing
        self.drawing = False  # Control continuous drawing state
        self.smooth_delay = 10  # Delay for smoother drawing in ms
        self.erase_on=False

    def draw_dot(self,event):
        """Draw a single dot at the given coordinates. Don't even know why I implemented this"""
        x,y=event.x,event.y
        self.canvas.create_oval(
            x - self.radius, y - self.radius, x + self.radius, y + self.radius,
            fill=self.selected_color, outline=""
        )

    def choose_color(self):
        """Open color chooser dialog and set the selected color."""
        color = colorchooser.askcolor(title="Choose a color")
        if color[1]:  # colorchooser returns (RGB, hex) tuple; hex value is at index 1
            self.selected_color = color[1]

    def start_draw(self, event):
        """Initialize points list on mouse click and start drawing."""
        self.points = [(event.x, event.y)]
        self.last_x, self.last_y = event.x, event.y
        self.drawing = True  # Enable drawing
        self.draw_line_buffer()  # Start continuous drawing

    def stop_drawing(self, event):
        """Stop drawing when the mouse button is released."""
        self.drawing = False  # Disable drawing

    def track_mouse(self, event):
        """Track mouse movement for drawing."""
        if self.drawing:
            x, y = event.x, event.y
            # Only add points if the distance is greater than 3 pixels
            if math.dist((self.last_x, self.last_y), (x, y)) > 8:
                self.points.append((x, y))  # Add point to the buffer
                self.last_x, self.last_y = x, y

    def draw_line_buffer(self):
        """Draw lines through buffered points continuously for smoother effect. took way too long"""
        if self.drawing and len(self.points) > 1:
            # Draw a smooth line through all points in the buffer
            flat_points = self.flatten_points(self.points)
            if len(flat_points) >= 4:  # At least two points (4 coordinates) required
                self.canvas.create_line(
                    *flat_points,
                    fill=self.selected_color,
                    width=self.line_thickness,
                    smooth=True,
                    splinesteps=36  # Higher splinesteps for smoother curve
                )
            # Keep only the last point in the buffer to avoid redrawing the entire line
            self.points = [self.points[-1]]

        # Schedule the next draw call if still drawing
        if self.drawing:
            self.after(self.smooth_delay, self.draw_line_buffer)

    def flatten_points(self, points):
        """Convert list of tuples into a flat list for create_line"""
        return [coord for point in points for coord in point]  # Flatten list of tuples to a flat list of coordinates

    def update_thickness(self, event=None):
        """Update the radius based on the slider's value."""
        self.line_thickness = self.slider.get()
        self.radius=self.slider.get()

    def erase(self):
        """Why didn't I think of this earlier?"""
        self.erase_on=not self.erase_on
        if self.erase_on:
            self.selected_color=('white')
        elif not self.erase_on:
            self.selected_color='black'

    def clear_canvas(self):
        self.canvas.delete("all")

# Main application window setup
root = Tk()
root.title("Kevin's Canvas")

# Configure the main window to expand the ArtCanvas frame
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create and display the ArtCanvas
art_canvas = ArtCanvas(root)
art_canvas.grid(sticky="nsew")

# Run the Tkinter event loop
root.mainloop()


