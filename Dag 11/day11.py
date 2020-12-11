import collections
import functools
import io
import itertools
import operator
import re
import sys

class Chair:
    def __init__(self):
        self.occupants = 0
        self.neighbours = []

    def __repr__(self):
        return "#" if self.occupants else "L"

def get_chairs(indata, sight_radius = -1):
    height = len(indata)
    width = len(indata[0])
    chair_map = {}
    directions = [(dy, dx) for dy in range(-1, 2) for dx in range(-1, 2) if dx != 0 or dy != 0]
    for y in range(height):
        for x in range(width):
            c = indata[y][x]
            if c != 'L':
                continue
            chair_map[y, x] = Chair()
    chairs = []
    for (y, x), chair in chair_map.items():
        for dy, dx in directions:
            sight_in_direction = sight_radius
            ydy = y + dy
            xdx = x + dx
            while sight_in_direction and ydy in range(height) and xdx in range(width):
                if (ydy, xdx) in chair_map:
                    chair.neighbours.append(chair_map[ydy, xdx])
                    break
                ydy += dy
                xdx += dx
                sight_in_direction -= 1
        chairs.append(chair)
    return chairs

def stabilise_chair_occupation(chairs, tolerance):
    active = set()
    for chair in chairs:
        if len(chair.neighbours) < tolerance:
            chair.occupants = 1
        else:
            active.add(chair)
    while active:
        changing = set()
        activated = set()
        for chair in active:
            if chair.occupants:
                remaining_tolerance = tolerance
                for neighbour in chair.neighbours:
                    remaining_tolerance -= neighbour.occupants
                    if not remaining_tolerance:
                        changing.add(chair)
                        activated.update(chair.neighbours)
                        break
            else:
                for neighbour in chair.neighbours:
                    if neighbour.occupants:
                        break
                else:
                    changing.add(chair)
                    activated.update(chair.neighbours)
        for chair in changing:
            chair.occupants = 1 - chair.occupants
        active = changing | activated

def first(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = [list(line.strip()) for line in infile]
    chairs = get_chairs(indata, 1)
    stabilise_chair_occupation(chairs, 4)
    print("First star: {}".format(sum([chair.occupants for chair in chairs])))

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = [list(line.strip()) for line in infile]
    chairs = get_chairs(indata, -1)
    stabilise_chair_occupation(chairs, 5)
    print("Second star: {}".format(sum([chair.occupants for chair in chairs])))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])