import random


class WaveFunctionCollapse:
    def __init__(self, tile_amount, grid_size=10):
        self._tile_amount = tile_amount
        self._grid_size = grid_size

        self._grid = [[0]*grid_size for _ in range(grid_size)]
        self._neighboring_tiles = []

    def first_gen(self):
        start_pos = (random.randint(0, self._grid_size - 1), random.randint(0, self._grid_size - 1))
        self._grid[start_pos[0]][start_pos[1]] = random.randint(1, self._tile_amount)
        self._neighboring_tiles = self.get_neighbors(start_pos[0], start_pos[1])

    def next_gen(self):
        for tile in self._neighboring_tiles:
            tile_neighbors = self.get_neighbors(tile[0], tile[1])
            
            self._grid[tile[0]][tile[1]] = 6

    def get_neighbors(self, x, y):
        return_list = []
        checks = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for check in checks:
            if 0 <= (x+check[0]) <= self._grid_size - 1 and 0 <= (y+check[1]) <= self._grid_size - 1:
                return_list.append((x+check[0], y+check[1]))

        return return_list

    def __str__(self):
        return_string = ""
        for line in self._grid:
            for index in range(len(line)):
                return_string += str(line[index]) + ("  " if index != self._grid_size-1 else "\n")
        return return_string


if __name__ == "__main__":

    wfc = WaveFunctionCollapse(4, 5)
    wfc.first_gen()
    wfc.next_gen()
    print(wfc)
