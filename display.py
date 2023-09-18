import tkinter as tk
from tkinter.font import Font
import random
from PIL import Image, ImageTk


class App(tk.Tk):
    grid_canvas_size = 600

    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.resizable(False, False)
        self.title("Wave Function Collapse")

        self.grid_x = grid_x
        self.grid_y = grid_y
        y_aspect_ratio = grid_y/grid_x

        """
        self.test_img = ImageTk.PhotoImage(Image.open("Capture.PNG").resize((int(App.grid_canvas_size/self.grid_size),
                                                                             int(App.grid_canvas_size/self.grid_size)),
                                                                             Image.LANCZOS))
        """
        self.test_colors = ["deep sky blue", "bisque", "pale green", "medium sea green"]

        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(side=tk.TOP)

        self.grid_canvas = tk.Canvas(self.grid_frame, height=App.grid_canvas_size + 1,
                                     width=App.grid_canvas_size + 1, borderwidth=0, highlightthickness=0)
        self.grid_canvas.pack()

    def test(self):
        for i in range(self.grid_x):
            for j in range(self.grid_y):
                app.draw_element(i, j, random.choice(self.test_colors))

    def set_values(self, collapsed_grid, use_colormap=False):
        for y_index, x_row in enumerate(collapsed_grid):
            for x_index, cell_value in enumerate(x_row):

                if use_colormap:
                    cell_value = use_colormap[cell_value]

                self.draw_element(x_index, y_index, cell_value)

    def draw_element(self, x, y, draw_object=None):
        factor = App.grid_canvas_size/max(self.grid_x, self.grid_y)

        if type(draw_object) == int:

            self.grid_canvas.create_text(x * factor + int(factor / 2), y * factor + int(factor / 2),
                                         font=Font(size=int(factor/2)), text=str(draw_object))

        elif type(draw_object) == str:
            self.grid_canvas.create_rectangle(x * factor, y * factor, (x + 1) * factor, (y + 1) * factor,
                                              fill=draw_object, outline=draw_object)

        elif type(draw_object) == ImageTk.PhotoImage:
            self.grid_canvas.create_image(x * factor, y * factor, anchor=tk.NW, image=draw_object)

        else:
            self.grid_canvas.create_rectangle(x * factor, y * factor, (x + 1) * factor, (y + 1) * factor, fill="white")


if __name__ == "__main__":
    app = App(16, 17)
    app.test()
    app.mainloop()