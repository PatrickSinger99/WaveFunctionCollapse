tiles = (1, 2, 3, 4)

tile_numbers = {tile: i for i, tile in enumerate(tiles)}
print(tile_numbers)

bitmask = 0
for tile in tile_numbers:
    bitmask |= 1 << tile_numbers[tile]

print(bitmask)
