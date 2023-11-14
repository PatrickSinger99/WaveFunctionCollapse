import tkinter as tk
from tkinter.font import Font
import random
from PIL import Image, ImageTk
from tile_widget import TileWidget


class App(tk.Tk):
    window_width = 600
    window_height = 400

    def __init__(self):
        super().__init__()

        # Window Parameters
        self.title("Wave Function Collapse")
        self.minsize(800, 400)
        self.geometry("1200x700")
        self.columnconfigure(1, weight=1)  # Set column 2 to scale with resizing window
        self.rowconfigure(1, weight=1)  # Set row 2 to scale with resizing window

        """CONFIG VARIABLES"""


        """WINDOW SECTIONS"""

        # FRAME: Header
        self.header_frame = tk.Frame(self, bg="grey", height=40)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="EW")
        self.header_frame.pack_propagate(False)

        # FRAME: Parameters
        self.parameter_frame = tk.Frame(self, bg="light grey", width=400)
        self.parameter_frame.grid(row=1, column=0, rowspan=2, sticky="NS")
        self.parameter_frame.pack_propagate(False)

        # FRAME: Display
        self.display_frame = tk.Frame(self, bg="white")
        self.display_frame.grid(row=1, column=1)

        # FRAME: ACTION PANEL
        self.download_frame = tk.Frame(self, bg="grey", height=40)
        self.download_frame.grid(row=2, column=1, sticky="EW")

        """HEADER"""

        # Title
        tk.Label(self.header_frame, text="Placeholder Title", font=Font(size=12), bg=self.header_frame.cget("bg")).pack(side="left")

        """PARAMETERS"""

        # FRAME: General Settings
        self.general_settings_frame = tk.Frame(self.parameter_frame, bg=self.parameter_frame.cget("bg"))
        self.general_settings_frame.pack(side="top", fill="x")
        tk.Label(self.general_settings_frame, text="General Settings", anchor="w", font=Font(size=10, weight="bold"),
                 bg=self.general_settings_frame.cget("bg")).grid(row=0, column=0, columnspan=2, sticky="EW")

        # Grid size setting
        tk.Label(self.general_settings_frame, text="Grid Size", bg=self.general_settings_frame.cget("bg")).grid(row=1, column=0, padx=(0, 20), sticky="W")

        self.grid_size_settings_control_frame = tk.Frame(self.general_settings_frame, bg=self.general_settings_frame.cget("bg"))
        self.grid_size_settings_control_frame.grid(row=1, column=1)

        tk.Label(self.grid_size_settings_control_frame, text="X", bg=self.general_settings_frame.cget("bg")).pack(side="left")
        self.grid_size_x_variable = tk.StringVar()
        self.grid_size_x_entry = tk.Entry(self.grid_size_settings_control_frame, textvariable=self.grid_size_x_variable,
                                          width=5, validate='all', validatecommand=(self.register(self.validate_number_entry), '%P'))
        self.grid_size_x_entry.pack(side="left")

        tk.Label(self.grid_size_settings_control_frame, text="Y", bg=self.general_settings_frame.cget("bg")).pack(side="left")
        self.grid_size_y_variable = tk.StringVar()
        self.grid_size_y_entry = tk.Entry(self.grid_size_settings_control_frame, textvariable=self.grid_size_y_variable,
                                          width=5, validate='all', validatecommand=(self.register(self.validate_number_entry), '%P'))
        self.grid_size_y_entry.pack(side="left")

        # Periodic setting
        tk.Label(self.general_settings_frame, text="Repeating Pattern", bg=self.general_settings_frame.cget("bg")).grid(row=2, column=0, padx=(0, 20), sticky="W")

        self.periodic_variable = tk.BooleanVar()
        self.periodic_button = tk.Checkbutton(self.general_settings_frame, variable=self.periodic_variable,
                                              bg=self.general_settings_frame.cget("bg"), activebackground=self.general_settings_frame.cget("bg"))
        self.periodic_button.grid(row=2, column=1, sticky="W")

        # FRAME: Tile Settings
        self.tile_settings_frame = tk.Frame(self.parameter_frame, bg=self.parameter_frame.cget("bg"))
        self.tile_settings_frame.pack(side="top", fill="both", expand=True)
        tk.Label(self.tile_settings_frame, text="Tile Settings", anchor="w", font=Font(size=10, weight="bold"),
                 bg=self.tile_settings_frame.cget("bg")).pack(side="top", pady=(15, 0), anchor="w")

        # BUTTON: Add tile
        self.add_tile_button = tk.Button(self.tile_settings_frame, text="Add Tile", command=self.add_tile)
        self.add_tile_button.pack(side="top")

        """SETUP SCROLLABLE AREA"""

        # Create canvas as wrapper for scroll widgets
        self.scrollable_canvas = tk.Canvas(self.tile_settings_frame, bg=self.tile_settings_frame.cget("bg"),
                                           highlightthickness=0, relief='ridge')

        # Frame inside canvas
        self.scrollable_frame = tk.Frame(self.scrollable_canvas, bg=self.scrollable_canvas.cget("bg"))
        self.scrollable_frame.pack(side="left")
        self.scrollable_frame.bind("<Configure>", lambda e: self.scrollable_canvas.configure(scrollregion=self.scrollable_canvas.bbox("all")))

        # Scrollbar for canvas
        self.scrollbar = tk.Scrollbar(self.scrollable_canvas, orient="vertical", command=self.scrollable_canvas.yview,
                                      troughcolor=self.scrollable_canvas.cget("bg"))
        self.scrollbar.pack(side="right", fill="y")

        # Add a window with inner frame inside canvas. Link scrollbar to canvas
        self.scrollable_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_canvas.pack(side="bottom", fill="both", expand=True)

        # Bind scrollwheel to canvas to enable scrolling with mouse
        self.scrollable_frame.bind("<Enter>", lambda x: self.bind_canvas_to_mousewheel(self.scrollable_canvas))
        self.scrollable_frame.bind("<Leave>", lambda x: self.unbind_canvas_from_mousewheel(self.scrollable_canvas))

    def add_tile(self):
        # Add new tile widget to canvas and widget list
        new_tile = self.create_tile()
        new_tile.pack(side="top", padx=5, pady=(0, 5))

        # Move down scroll area to new element
        self.after(10, lambda: self.scrollable_canvas.yview_moveto(1))

    def create_tile(self):
        width_of_tile = self.scrollable_canvas.winfo_width() - self.scrollbar.winfo_width() - 10  # 10 is padding
        new_tile_frame = TileWidget(master=self.scrollable_frame, master_root=self, width=width_of_tile)

        return new_tile_frame

    def bind_canvas_to_mousewheel(self, canvas):
        # Bind mousewheel only if more elements are available than fit the screen
        if self.scrollable_frame.winfo_height() > self.scrollable_canvas.winfo_height():
            canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    @staticmethod
    def unbind_canvas_from_mousewheel(canvas):
        canvas.unbind_all("<MouseWheel>")

    def on_mousewheel(self, event):
        self.scrollable_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    @staticmethod
    def validate_number_entry(entry):
        # Only register new keystroke if new entry value is numeric and no langer than 3 numbers
        if (str.isdigit(entry) or entry == "") and len(entry) < 4:
            return True
        return False

    def get_current_tile_states(self):
        current_tile_states = {}
        for widget in self.scrollable_frame.winfo_children():
            current_tile_states[widget.id] = {"color": widget.tile_appearance}

        return current_tile_states


if __name__ == '__main__':
    app = App()

    app.mainloop()
