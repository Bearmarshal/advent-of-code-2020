import collections
import enum
import functools
import io
import itertools
import math
import operator
import re
import sys

def first(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    tile_regex = re.compile(r'Tile (?P<tile_id>\d+):\n(?P<tile_data>(?:[#.]+\n)+)')
    tiles_by_border = {}
    tile_neighbours = {}
    for match in tile_regex.finditer(indata):
        tile_id = int(match['tile_id'])
        tile_neighbours[tile_id] = []
        tile_rows = match['tile_data'].strip().split('\n')
        tile_rows_transposed = list(map(''.join, zip(*tile_rows)))
        for border in tile_rows[0], tile_rows[-1], tile_rows_transposed[0], tile_rows_transposed[-1]:
            if border in tiles_by_border:
                neighbour_id = tiles_by_border[border]
                tile_neighbours[tile_id].append(neighbour_id)
                tile_neighbours[neighbour_id].append(tile_id)
            elif border[::-1] in tiles_by_border:
                neighbour_id = tiles_by_border[border[::-1]]
                tile_neighbours[tile_id].append(neighbour_id)
                tile_neighbours[neighbour_id].append(tile_id)
            else:
                tiles_by_border[border] = tile_id
    print("First star: {}".format(functools.reduce(operator.mul, [tile_id for tile_id, neighbours in tile_neighbours.items() if len(neighbours) == 2])))

def all_orientations_of(tile):
    yield tile
    yield tile[::-1]
    tile_mirrored = tuple((row[::-1] for row in tile))
    yield tile_mirrored
    yield tile_mirrored[::-1]
    tile_transposed = tuple(map(''.join, zip(*tile)))
    yield tile_transposed
    yield tile_transposed[::-1]
    tile_transposed_mirrored = tuple((row[::-1] for row in tile_transposed))
    yield tile_transposed_mirrored
    yield tile_transposed_mirrored[::-1]

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    tile_regex = re.compile(r'Tile (?P<tile_id>\d+):\n(?P<tile_data>(?:[#.]+\n)+)')
    sea_monster = (
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ")
    sea_monster_regex = re.compile('\n'.join(sea_monster).replace(' ', '.'))
    tiles_by_border = {}, {}, {}, {} # top, left, bottom, right
    tile_neighbours = {}
    number_of_tiles = 0
    border_getters = [lambda t: t[0], lambda t: ''.join(r[0] for r in t), lambda t: t[-1], lambda t: ''.join(r[-1] for r in t)]
    for match in tile_regex.finditer(indata):
        number_of_tiles += 1
        tile_rows = tuple(match['tile_data'].strip().split('\n'))
        to_add_to_tiles_by_border = {}, {}, {}, {}
        for tile in all_orientations_of(tile_rows):
            tile_image = tuple((row[1:-1] for row in tile[1:-1]))
            tile_neighbours[tile_image] = [None, None, None, None]
            for alignment in range(4):
                alignment_inverse = (alignment + 2) % 4
                if (border := border_getters[alignment](tile)) in tiles_by_border[alignment_inverse]:
                    neighbour_image = tiles_by_border[alignment_inverse][border]
                    tile_neighbours[tile_image][alignment] = neighbour_image
                    tile_neighbours[neighbour_image][alignment_inverse] = tile_image
                else:
                    to_add_to_tiles_by_border[alignment][border] = tile_image
        list(itertools.starmap(dict.update, zip(tiles_by_border, to_add_to_tiles_by_border)))
    for tile, neighbours in tile_neighbours.items():
        if not neighbours[0] and not neighbours[1]:
            top_left_corner = tile
            break
    tile_width = len(top_left_corner)
    image_tile_width = int(math.sqrt(number_of_tiles))
    image_width = image_tile_width * tile_width
    image = [" " * image_width for _ in range(image_width)]
    tile = top_left_corner
    for y in range(image_tile_width):
        first_tile_in_row = tile
        y_offset = y * tile_width
        for x in range(image_tile_width):
            x_offset = x * tile_width
            image[y_offset : y_offset + tile_width] = [image_row[0:x_offset] + tile_row + image_row[x_offset + tile_width : image_width] for image_row, tile_row in zip(image[y_offset : y_offset + tile_width], tile)]
            tile = tile_neighbours[tile][3]
        tile = tile_neighbours[first_tile_in_row][2]
    sea_monster_height = len(sea_monster)
    sea_monster_width = len(sea_monster[0])
    num_sea_monsters = 0
    for oriented_image in all_orientations_of(image):
        print('\n'.join(oriented_image))
        print()
        for y in range(image_width + 1 - sea_monster_height):
            rows = oriented_image[y : y + sea_monster_height]
            for x in range(image_width + 1  - sea_monster_width):
                outtake = '\n'.join([row[x : x + sea_monster_width] for row in rows])
                if sea_monster_regex.fullmatch(outtake):
                    num_sea_monsters += 1
        if num_sea_monsters:
            break
    lumber_yards_in_sea_monster = ''.join(sea_monster).count('#')
    lumber_yards_in_sea = ''.join(oriented_image).count('#')
    print("Second star: {}".format(lumber_yards_in_sea - num_sea_monsters * lumber_yards_in_sea_monster))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])