import collections
import enum
import functools
import io
import itertools
import operator
import re
import sys

class Rotation(enum.Enum):
    R = +1
    L = -1

    def distance(self, degrees):
        return self.value * int(degrees / 90)

    def rotate(self, vector, degrees):
        distance = self.distance(degrees) % 4
        if distance == 1:
            return vector[1], -vector[0]
        elif distance == 2:
            return -vector[0], -vector[1]
        elif distance == 3:
            return -vector[1], vector[0]
        else:
            return vector


class Direction(enum.Enum):
    E = 0, 1
    S = 1, 0
    W = 0, -1
    N = -1, 0

    def rotate(self, rotation, degrees):
        return list(Direction)[(list(Direction).index(self) + rotation.distance(degrees)) % len(Direction)]

    def move(self, position, distance):
        return tuple((coordinate + direction * distance for coordinate, direction in zip(position, self.value)))

def first(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    regex = re.compile(r'(?:(?P<direction>[ESWN])|(?P<rotation>[RL])|(?P<forward>[F]))(?P<amount>\d+)')
    direction = Direction.E
    position = 0, 0
    for match in regex.finditer(indata):
        amount = int(match['amount'])
        if match['direction']:
            position = Direction[match['direction']].move(position, amount)
        if match['rotation']:
            rotation = Rotation[match['rotation']]
            direction = direction.rotate(rotation, amount)
        if match['forward']:
            position = direction.move(position, amount)
    print("First star: {}".format(sum(map(operator.abs, position))))

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    regex = re.compile(r'(?:(?P<direction>[ESWN])|(?P<rotation>[RL])|(?P<forward>[F]))(?P<amount>\d+)')
    waypoint = -1, 10
    position = 0, 0
    for match in regex.finditer(indata):
        amount = int(match['amount'])
        if match['direction']:
            waypoint = Direction[match['direction']].move(waypoint, amount)
        if match['rotation']:
            waypoint = Rotation[match['rotation']].rotate(waypoint, amount)
        if match['forward']:
            position = tuple((coordinate + direction * amount for coordinate, direction in zip(position, waypoint)))
    print("Second star: {}".format(sum(map(operator.abs, position))))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])