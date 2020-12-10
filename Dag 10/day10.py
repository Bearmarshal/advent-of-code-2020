import collections
import functools
import io
import operator
import re
import sys

def first(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = [int(line) for line in infile]
    indata.sort()
    distance_nums = {}
    for distance in map(lambda pair: operator.sub(*pair), zip(indata + [indata[-1] + 3], [0] + indata)):
        distance_nums[distance] = (distance_nums.get(distance, 0) + 1)
    print("First star: {}".format(distance_nums[1] * distance_nums[3]))

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = [int(line) for line in infile]
    print("Second star: {}".format())

if __name__ == "__main__":
    first(sys.argv[1])
    # second(sys.argv[1])