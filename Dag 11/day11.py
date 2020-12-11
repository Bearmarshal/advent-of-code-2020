import collections
import functools
import io
import itertools
import operator
import re
import sys

class Chair:
    def __init__(self):
        self.occupants = 1
        self.neighbours = []

def first(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = [list(line.strip()) for line in infile]
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
    state = []
    for (y, x), chair in chair_map.items():
        for dy, dx in directions:
            ydy = y + dy
            xdx = x + dx
            if (ydy, xdx) in chair_map:
                chair.neighbours.append(chair_map[ydy, xdx])
        if len(chair.neighbours) >= 4:
            state.append(chair)
    state_modified = True
    while state_modified:
        state_modified = False
        seen_occupants = [(chair, sum([neighbour.occupants for neighbour in chair.neighbours])) for chair in state]
        for chair, num_seen in seen_occupants:
            if chair.occupants == 0 and num_seen == 0:
                chair.occupants = 1
                state_modified = True
            elif chair.occupants == 1 and num_seen >= 4:
                chair.occupants = 0
                state_modified = True
    print("First star: {}".format(sum([chair.occupants for chair in chair_map.values()])))

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = [list(line.strip()) for line in infile]
    height = len(indata)
    width = len(indata[0])
    board = [[[c, 0, []] for c in row] for row in indata]
    state = []
    directions = [(dy, dx) for dy in range(-1, 2) for dx in range(-1, 2) if dx != 0 or dy != 0]
    for y in range(height):
        for x in range(width):
            chair = board[y][x]
            if chair[0] not in 'L#':
                continue
            for dy, dx in directions:
                ydy = y + dy
                xdx = x + dx
                while ydy >= 0 and ydy < height and xdx >= 0 and xdx < width:
                    if board[ydy][xdx][0] in 'L#':
                        chair[2] += [board[ydy][xdx]]
                        break
                    ydy += dy
                    xdx += dx
            state += [chair]
    state_modified = True
    while state_modified:
        state_modified = False
        for chair in state:
            chair[1] = len([c for c, _, _ in chair[2] if c == '#'])
        for chair in state:
            if chair[0] == 'L' and chair[1] == 0:
                chair[0] = '#'
                state_modified = True
            elif chair[0] == '#' and chair[1] >= 5:
                chair[0] = 'L'
                state_modified = True
    print("Second star: {}".format(len([c for c, _, _ in state if c == '#'])))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])