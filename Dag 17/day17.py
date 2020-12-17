import collections
import functools
import io
import itertools
import operator
import re
import sys

def directions(num_dimensions = 3):
    return (tuple(vector) for vector in itertools.product((-1, 0, 1), repeat = num_dimensions) if functools.reduce(operator.or_, vector))

def neighbouring_coordinates(position):
    for vector in directions(num_dimensions = len(position)):
        yield tuple(itertools.starmap(operator.add, zip(position, vector)))

class ConwayCube:
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
                neighbour = cube_map.setdefault(neigbour_coords, ConwayCube(neigbour_coords))
                if not neighbour.fully_inited:
                    neighbour.neighbours.add(self)
                    self.neighbours.add(neighbour)
            self.fully_inited = True

    def get_next_state(self):
        sum_neighbours = sum((neighbour.state for neighbour in self.neighbours))
        if self.state == 0:
            return 1 if sum_neighbours == 3 else 0
        else:
            return 1 if sum_neighbours in (2, 3) else 0

class CubeGrid:
    def __init__(self, num_dimensions = 3):
        self.cube_map = {}
        self.num_dimensions = num_dimensions

    def populate(self, indata):
        height = len(indata)
        width = len(indata[0])
        higher_dimensions = [0] * (self.num_dimensions - 2)
        for y in range(height):
            for x in range(width):
                if indata[y][x] == '#':
                    position = (x, y, *higher_dimensions)
                    cube = self.cube_map.setdefault(position, ConwayCube(position))
                    cube.state = 1
                    cube.init_fully(self.cube_map)

    def tick(self):
        new_states = {cube: cube.get_next_state() for cube in self.cube_map.values()}
        for cube, new_state in new_states.items():
            cube.state = new_state
            if new_state == 1 and not cube.fully_inited:
                cube.init_fully(self.cube_map)

def first(file_name):
    cube_grid = CubeGrid()
    with io.open(file_name, mode = 'r') as infile:
        indata = [list(line.strip()) for line in infile]
    cube_grid.populate(indata)
    for _ in range(6):
        cube_grid.tick()
    print("First star: {}".format(sum((cube.state for cube in cube_grid.cube_map.values()))))

def second(file_name):
    cube_grid = CubeGrid(4)
    with io.open(file_name, mode = 'r') as infile:
        indata = [list(line.strip()) for line in infile]
    cube_grid.populate(indata)
    for _ in range(6):
        cube_grid.tick()
    print("Second star: {}".format(sum((cube.state for cube in cube_grid.cube_map.values()))))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])