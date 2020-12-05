import functools
import io
import operator
import sys

def first(file_name):
    x = 0
    dx = 3
    num_trees = 0
    width = None
    with io.open(file_name) as infile:
        for line in infile:
            line = line.strip()
            if width == None:
                width = len(line)
            num_trees += line[x].count('#')
            x += dx
            x %= width
    print("First star: {}".format(num_trees))

def second(file_name):
    x = (0, 0, 0, 0, 0)
    y = 0
    dx = (1, 3, 5, 7, 1)
    dy = (1, 1, 1, 1, 2)
    num_trees = (0, 0, 0, 0, 0)
    width = None
    with io.open(file_name) as infile:
        for line in infile:
            line = line.strip()
            if width == None:
                width = len(line)
            num_trees = [ti + line[xi].count('#') if y % dyi == 0 else ti for ti, xi, dyi in zip(num_trees, x, dy)]
            x = [(xi + dxi) % width if y % dyi == 0 else xi for xi, dxi, dyi in zip(x, dx, dy)]
            y += 1
    print("Second star: {}".format(functools.reduce(operator.mul, num_trees)))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])