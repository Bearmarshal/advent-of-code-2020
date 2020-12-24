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
        indata = [line.strip() for line in infile]
    directions = {'e': (1, 0), 'se': (1, 1), 'sw': (0, 1), 'w': (-1, 0), 'nw': (-1, -1), 'ne': (0, -1)}
    directions_regex = re.compile(r'[sn]?[ew]')
    black_tiles = set()
    for line in indata:
        x, y = 0, 0
        for step in directions_regex.findall(line):
            dx, dy = directions[step]
            x += dx
            y += dy
        if (x, y) not in black_tiles:
            black_tiles.add((x, y))
        else:
            black_tiles.remove((x, y))
    result = len(black_tiles)
    print("First star: {}".format(result))

def directions(num_dimensions = 2):
    return (tuple(vector) for vector in itertools.product((-1, 0, 1), repeat = num_dimensions) if sum(vector))

def neighbouring_coordinates(position):
    for vector in directions(num_dimensions = len(position)):
        yield tuple(itertools.starmap(operator.add, zip(position, vector)))

class ConwayHex:
    def __init__(self, position):
        self.position = position
        self.state = 0
        self.neighbours = set()
        self.fully_inited = False

    def __repr__(self):
        return "#" if self.state == 1 else "."

    def init_fully(self, cube_map):
        if not self.fully_inited:
            for neigbour_coords in neighbouring_coordinates(self.position):
                neighbour = cube_map.setdefault(neigbour_coords, ConwayHex(neigbour_coords))
                if not neighbour.fully_inited:
                    neighbour.neighbours.add(self)
                    self.neighbours.add(neighbour)
            self.fully_inited = True

    def get_next_state(self):
        sum_neighbours = sum((neighbour.state for neighbour in self.neighbours))
        if self.state == 0:
            return 1 if sum_neighbours == 2 else 0
        else:
            return 1 if sum_neighbours in (1, 2) else 0

class HexGrid:
    def __init__(self, num_dimensions = 2):
        self.hex_map = {}
        self.num_dimensions = num_dimensions

    def populate(self, indata):
        directions = {'e': (1, 0), 'se': (1, 1), 'sw': (0, 1), 'w': (-1, 0), 'nw': (-1, -1), 'ne': (0, -1)}
        directions_regex = re.compile(r'[sn]?[ew]')
        black_tiles = set()
        for line in indata:
            x, y = 0, 0
            for step in directions_regex.findall(line):
                dx, dy = directions[step]
                x += dx
                y += dy
            if (x, y) not in black_tiles:
                black_tiles.add((x, y))
            else:
                black_tiles.remove((x, y))
        for position in black_tiles:
            hex = self.hex_map.setdefault(position, ConwayHex(position))
            hex.state = 1
            hex.init_fully(self.hex_map)

    def tick(self):
        new_states = {hex: hex.get_next_state() for hex in self.hex_map.values()}
        for hex, new_state in new_states.items():
            hex.state = new_state
            if new_state == 1 and not hex.fully_inited:
                hex.init_fully(self.hex_map)

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = [line.strip() for line in infile]
    floor = HexGrid()
    floor.populate(indata)
    for _ in range(100):
        floor.tick()
    result = sum(hex.state for hex in floor.hex_map.values())
    print("Second star: {}".format(result))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])