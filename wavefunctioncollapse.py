import random
from copy import deepcopy
import math
import time
from typing import List, Dict, Tuple, Union


class WaveFunctionCollapse:
    def __init__(self, width, height, tiles: Union[List, Tuple], tile_neighbors: Dict[int, List],
                 tile_weights: Dict[int, int]):
        # Grid
        self.width = width
        self.height = height
        self.grid = []

        # Tile infos
        self.tiles = tiles  # Example: (1, 2, 3, 4)
        self.tile_neighbors = tile_neighbors  # Example: {1: [1, 2], 2: [1, 2, 3], 3: [2, 3, 4], 4: [3, 4]}
        self.tile_weights = tile_weights  # Example: {1: 10, 2: 20, 3: 10, 4: 5}

        # Init functions
        self.create_grid()

    def __str__(self):
        return_str = ""
        for row in self.grid:
            for state in row:
                if len(state) == 1:
                    return_str += (str(state[0]) + " ")
                else:
                    return_str += "* "
            return_str += "\n"
        return return_str

    def create_grid(self):
        """
        Generates the grid based on the class parameters.
        """
        self.grid = [[list(self.tiles) for _ in range(self.width)] for _ in range(self.height)]

    def get_neighbors(self, x, y):
        """
        Gets all neighbors for given coordinates. Checks for boundary edgecases.
        :param x: X coordinate of the cell.
        :param y: Y coordinate of the cell.
        :return: coorinates of all valid neighbors [(x,y), (x,y), ...].
        """
        indices = []
        # Upper x row
        if x > 0:
            indices.append((x-1, y))

        # Lower x row
        if x < self.width-1:
            indices.append((x+1, y))

        # Column before
        if y > 0:
            indices.append((x, y-1))

        # Column after
        if y < self.height-1:
            indices.append((x, y+1))

        return indices

    def next_generation(self):
        """
        Facilitates one generation of the wave function collapse including the following steps:
            1. Collapse cell with lowest entropy.
            2. Update whole grid based on new neighbor states.
        :return: Array of grid entropies; Boolean if whole generation is finished (All states are collapsed)
        """

        # Get cell with lowest entropy
        grid_entropies, cell_coords = self.get_lowest_entropy_cell()

        # End run and return is finished if no cell to collapse could be found
        if cell_coords is None:
            return grid_entropies, True

        # Else if cell cound be found, collapse it
        x_index, y_index = cell_coords
        cell_weights = [self.tile_weights[tile] for tile in self.grid[y_index][x_index]]
        self.grid[y_index][x_index] = random.choices(self.grid[y_index][x_index], weights=cell_weights)

        # Loop over grid updates as long as changes appear
        changes_count = 1
        while changes_count != 0:
            changes_count = self.update_grid()

        # Return that run is not finished
        return grid_entropies, False

    def update_grid(self):
        """
        Iterates over every cell once and updates the state superpositions based on its neighbors.
        :return: Number of changed that where made to the states superpositions during the update.
        """
        changes_count = 0

        # Iterate through every cell in the grid
        for y_index, x_row in enumerate(self.grid):
            for x_index, cell_state in enumerate(x_row):

                # Iterate over every neighbor of a cell
                for x_neighbor, y_neighbor in self.get_neighbors(x_index, y_index):

                    # Aggregate all values that need to be removed from the possible states of the cell
                    to_remove = []
                    neighbor_vals = self.grid[y_neighbor][x_neighbor]

                    # Check for every possible cell value, if it can be placed besides all possible neighbor cells
                    for cell_value in self.grid[y_index][x_index]:
                        valid_neighbors_of_neighbor = set(sum([self.tile_neighbors[val] for val in neighbor_vals], []))

                        if cell_value not in valid_neighbors_of_neighbor:
                            to_remove.append(cell_value)

                    # Remove all impossible states for current cell
                    for val in to_remove:
                        self.grid[y_index][x_index].remove(val)
                        changes_count += 1

        # Return amount of changes made
        return changes_count

    def get_lowest_entropy_cell(self):
        """
        Calculates the entropies for current grid and selects a cell with the lowest entropy.
        :return: grid of entropies for every state; cell coordinates (x, y) for chosen cell with lowest entropy.
        """
        grid_entropies = deepcopy(self.grid)
        lowest_entropy = math.inf

        # Calculate entropies  TODO later also needs to consider cell probailities
        for y_index, x_row in enumerate(grid_entropies):
            for x_index, cell_state in enumerate(x_row):

                # Get entropy for cell
                if len(cell_state) != 1:  # Only check if cell not collapsed yet
                    cell_entropy = len(cell_state)
                    grid_entropies[y_index][x_index] = cell_entropy
                    # If entropy is lowest, save as lowest entropy
                    if cell_entropy < lowest_entropy:
                        lowest_entropy = cell_entropy
                else:
                    # If cell is already collapsed save entropy as none
                    grid_entropies[y_index][x_index] = None

        # Get all cells with lowest entropy
        lowest_entropy_cells = []
        for y_index, x_row in enumerate(grid_entropies):
            for x_index, cell_entropy in enumerate(x_row):
                if cell_entropy == lowest_entropy:
                    lowest_entropy_cells.append((x_index, y_index))

        # Return entropy grid and chosen lowest entropy cell coords
        if len(lowest_entropy_cells) > 0:
            chosen_cell = random.choice(lowest_entropy_cells)
        else:
            chosen_cell = None
        return grid_entropies, chosen_cell

    def collapse(self, print_generations: bool = False, print_result: bool = True) -> List[List[int]]:
        """
        Main function for wave function collapse. Runs the whole process and returns a finished value grid.
        :param print_generations: Print grid after every generation.
        :param print_result: Print info and collapsed grid when finished.
        :return: 2d array containing collapsed values.
        """
        start_time = time.time()
        finished, generation = False, 0

        # Run next generation as long as changes appear
        while not finished:
            grid_entropies, finished = self.next_generation()
            generation += 1
            if print_generations:
                print(f"Generation {generation}:\n{self}")

        # Print result if defined
        if print_result:
            print(f"Grid collapse finished after {generation} generations ({round(time.time()-start_time, 2)}s).")
            print("Resulting grid:\n" + str(self))

        # Return collapsed grid. Remove most inner list, as all values collapsed
        return_grid = deepcopy(self.grid)
        for y_index, x_row in enumerate(return_grid):
            for x_index in range(len(x_row)):
                return_grid[y_index][x_index] = return_grid[y_index][x_index][0]
        return return_grid


if __name__ == '__main__':
    ex_tiles = (1, 2, 3, 4)
    ex_tile_neighbors = {1: [1, 2], 2: [1, 2, 3], 3: [2, 3, 4], 4: [3, 4]}
    ex_tile_weights = {1: 30, 2: 25, 3: 25, 4: 30}
    w = WaveFunctionCollapse(16, 9, ex_tiles, ex_tile_neighbors, ex_tile_weights)
    w.collapse()
