from wavefunctioncollapse import WaveFunctionCollapse
from display import App

if __name__ == '__main__':

    x_dim, y_dim = 24, 24
    tiles = (1, 2, 3, 4, 5)
    tile_neighbors = {1: [1, 2], 2: [1, 2, 3], 3: [2, 3, 4], 4: [3, 4, 5], 5: [4]}
    tile_weights = {1: 30, 2: 25, 3: 25, 4: 30, 5: 30}
    colormap = {1: "deep sky blue", 2: "bisque", 3: "pale green", 4: "medium sea green", 5: "brown"}

    # Wave function collapse init
    wfc = WaveFunctionCollapse(x_dim, y_dim, tiles, tile_neighbors, tile_weights)

    # Run standard and display result

    collapsed_grid = wfc.collapse()
    app = App(x_dim, y_dim)
    app.set_values(collapsed_grid, use_colormap=colormap)
    app.mainloop()
    """
    # TEMP: Run with gui every step
    app = App(x_dim, y_dim)
    app.display_collapse(wavefunctioncollapse_class_instance=wfc, colormap=colormap)
    app.mainloop()
    """