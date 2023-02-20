import random


class WaveFunctionCollapse:
    def __init__(self, tile_amount, grid_size=10):
        self._tile_amount = tile_amount
        self._grid_size = grid_size

        self._grid = [[0]*grid_size for _ in range(grid_size)]
        self._next_gen_rel_tiles = []

    def first_gen(self):
        start_pos = (random.randint(0, self._grid_size - 1), random.randint(0, self._grid_size - 1))
        self._grid[start_pos[0]][start_pos[1]] = random.randint(1, self._tile_amount)
        self._next_gen_rel_tiles = self.get_neighbors(start_pos[0], start_pos[1])

    def next_gen(self):
        new_next_gen_rel_tiles = []
        for tile in self._next_gen_rel_tiles:
            new_next_gen_rel_tiles += self.get_neighbors(tile[0], tile[1])
            possible_values = self.get_possible_values_based_on_neighbors(tile[0], tile[1])

            if self._grid[tile[0]][tile[1]] == 0:
                self._grid[tile[0]][tile[1]] = random.choice(possible_values)

        self._next_gen_rel_tiles = new_next_gen_rel_tiles

    def run_simulation(self, show_prints=False):
        self.first_gen()
        last_gen_grid = None
        while last_gen_grid != self._grid:
            self.next_gen()

            if show_prints:
                print(self)

            last_gen_grid = 


    def get_neighbors(self, x, y):
        return_list = []
        checks = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for check in checks:
            if 0 <= (x+check[0]) <= self._grid_size - 1 and 0 <= (y+check[1]) <= self._grid_size - 1:
                return_list.append((x+check[0], y+check[1]))

        return return_list

    def get_possible_values_based_on_neighbors(self, x, y):
        possibility_space = [i+1 for i in range(self._tile_amount)]
        neighbors = self.get_neighbors(x, y)

        for neighbor_x, neighbor_y in neighbors:
            if self._grid[neighbor_x][neighbor_y] != 0:

                new_possibility_space = []
                for value in possibility_space:
                    if self._grid[neighbor_x][neighbor_y]-1 <= value <= self._grid[neighbor_x][neighbor_y]+1:
                        new_possibility_space.append(value)

                possibility_space = new_possibility_space

        return possibility_space

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
    wfc.next_gen()
    print(wfc)
    wfc.next_gen()
    print(wfc)
