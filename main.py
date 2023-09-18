from wavefunctioncollapse import WaveFunctionCollapse
from display import App

if __name__ == '__main__':
    x_dim, y_dim = 64, 64
    colormap = {1: "deep sky blue", 2: "bisque", 3: "pale green", 4: "medium sea green"}

    wfc = WaveFunctionCollapse(x_dim, y_dim)
    collapsed_grid = wfc.collapse()

    app = App(x_dim, y_dim)
    app.set_values(collapsed_grid, use_colormap=colormap)
    app.mainloop()

