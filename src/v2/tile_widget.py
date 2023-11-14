import tkinter as tk
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk


class TileWidget(tk.Frame):
    tile_id_counter = 0

    default_name = "New Tile"
    default_color = "#0022ff"

    button_color = "white"

    def __init__(self, master_root, tile_name=None, **kwargs):
        super().__init__(**kwargs)
        self.master_root = master_root

        # Add id and increment counter
        self.id = TileWidget.tile_id_counter
        TileWidget.tile_id_counter += 1

        if tile_name is None:
            tile_name = TileWidget.default_name

        self.tile_name = tile_name
        self.tile_appearance = TileWidget.default_color
        self.temp_other_tile_colors = {}  # Temporarily store colors for neighbor selection screen

        # FRAME: Tile Header
        self.tile_header_frame = tk.Frame(self, height=20, width=self.cget("width"), bg="grey")
        self.tile_header_frame.pack_propagate(False)
        self.tile_header_frame.pack(side="top", fill="x")

        # Tile Name display in header
        self.tile_index = tk.Label(self.tile_header_frame, text=f"New Tile", bg=self.tile_header_frame.cget("bg"))
        self.tile_index.pack(side="left")

        # BUTTON: Remove tile
        self.remove_button = tk.Button(self.tile_header_frame, text="X", command=lambda: self.destroy())
        self.remove_button.pack(side="right")

        # FRAME: Tile Properties
        self.tile_properties_frame = tk.Frame(self)
        self.tile_properties_frame.pack(side="bottom", fill="x")

        self.tile_preview = tk.Canvas(self.tile_properties_frame, width=80, height=80, relief="ridge",
                                      highlightthickness=0, bg=self.tile_appearance)
        self.tile_preview.grid(row=0, column=0, columnspan=2)

        # BUTTON: Color Selection
        self.color_selection_button = tk.Button(self.tile_properties_frame, text="Color", relief="flat", cursor="hand2",
                                                command=lambda: self.set_tile_appearance(mode="color"), bd=0,
                                                bg=TileWidget.button_color)
        self.color_selection_button.grid(row=1, column=0, sticky="EW")

        # BUTTON: Image Selection
        self.image_selection_button = tk.Button(self.tile_properties_frame, text="Image", relief="flat", cursor="hand2",
                                                command=lambda: self.set_tile_appearance(mode="image"), bd=0,
                                                bg=TileWidget.button_color)
        self.image_selection_button.grid(row=1, column=1, sticky="EW")

        # FRAME: Tile neighbors selection
        self.tile_neighbors_frame = tk.Frame(self.tile_properties_frame, bg="blue")
        self.tile_neighbors_frame.grid(row=0, column=2, rowspan=2, sticky="NSEW")

        self.add_neighbor_button = tk.Button(self.tile_neighbors_frame, text="Add", command=self.add_neighbor)
        self.add_neighbor_button.pack()

    def set_tile_appearance(self, mode):
        if mode == "color":
            hex_code = colorchooser.askcolor(title="Choose color")[1]

            if hex_code is not None:
                # Reset canvas and add new color as background
                self.tile_preview.delete("all")
                self.tile_preview.configure(bg=str(hex_code))

                # set instance variable
                self.tile_appearance = hex_code

        elif mode == "image":
            file = askopenfilename()

            if file != "":
                # TODO
                print("Not yet implemented")

    def add_neighbor(self):
        current_tile_states = self.master_root.get_current_tile_states()
        self.temp_other_tile_colors = {}  # Reset temporary tile colors
        toplevel_selection = tk.Toplevel()

        tk.Label(toplevel_selection, text="Select possible neighbors:").pack(side="top")
        tile_selection_frame = tk.Frame(toplevel_selection)
        tile_selection_frame.pack(side="bottom")

        for tile_id in current_tile_states:
            # Create image based on color or img file
            pil_img = Image.new(mode="RGB", size=(50, 50), color=self.hex_to_rgb(current_tile_states[tile_id]["color"]))
            self.temp_other_tile_colors[tile_id] = ImageTk.PhotoImage(pil_img)

            new_button = tk.Button(tile_selection_frame, image=self.temp_other_tile_colors[tile_id])
            new_button.pack(side="right")

    @staticmethod
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))