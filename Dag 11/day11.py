import collections
import functools
import io
import itertools
import operator
import re
import sys

def first(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = [list(line.strip()) for line in infile]
    height = len(indata)
    width = len(indata[0])
    horizontal_wall = ['+'] + list(itertools.repeat('-', width)) + ['+']
    board = [horizontal_wall] + [['|'] + line + ['|'] for line in indata] + [horizontal_wall]
    state = [[[c, 0] for c in row] for row in board]
    state_modified = True
    while state_modified:
        state_modified = False
        for y in range(1, height + 1):
            for x in range(1, width + 1):
                if state[y][x][0] not in 'L#':
                    continue
                state[y][x][1] = len([c for row in state[y-1:y+2] for c, _ in row[x-1:x+2] if c == '#']) - (1 if state[y][x][0] == '#' else 0)
        for row in state[1:-1]:
            for chair in row[1:-1]:
                if chair[0] == 'L' and chair[1] == 0:
                    chair[0] = '#'
                    state_modified = True
                elif chair[0] == '#' and chair[1] >= 4:
                    chair[0] = 'L'
                    state_modified = True
    print("First star: {}".format(len([c for row in state for c, _ in row if c == '#'])))

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = [list(line.strip()) for line in infile]
    height = len(indata)
    width = len(indata[0])
    horizontal_wall = ['+'] + list(itertools.repeat('-', width)) + ['+']
    board = [horizontal_wall] + [['|'] + line + ['|'] for line in indata] + [horizontal_wall]
    state = [[[c, 0, []] for c in row] for row in board]
    state_modified = True
    directions = [(dy, dx) for dy in range(-1, 2) for dx in range(-1, 2) if dx != 0 or dy != 0]
    for y in range(1, height + 1):
            for x in range(1, width + 1):
                if state[y][x][0] not in 'L#':
                    continue
                for dy, dx in directions:
                    ydy = y + dy
                    xdx = x + dx
                    while ydy > 0 and ydy <= height and xdx > 0 and xdx <= width:
                        if state[ydy][xdx][0] in 'L#':
                            state[y][x][2] += [state[ydy][xdx]]
                            break
                        ydy += dy
                        xdx += dx
    while state_modified:
        state_modified = False
        for y in range(1, height + 1):
            for x in range(1, width + 1):
                if state[y][x][0] not in 'L#':
                    continue
                num_occupied = 0
                for c, _, _ in state[y][x][2]:
                    if c == '#':
                        num_occupied += 1
                state[y][x][1] = num_occupied
        for row in state[1:-1]:
            for chair in row[1:-1]:
                if chair[0] == 'L' and chair[1] == 0:
                    chair[0] = '#'
                    state_modified = True
                elif chair[0] == '#' and chair[1] >= 5:
                    chair[0] = 'L'
                    state_modified = True
    print("Second star: {}".format(len([c for row in state for c, _, _ in row if c == '#'])))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])