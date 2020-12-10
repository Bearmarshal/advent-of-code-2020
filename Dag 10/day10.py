import collections
import functools
import io
import itertools
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
    indata.sort()
    distinct_blocks = []
    current_block = []
    for distance in map(lambda pair: operator.sub(*pair), zip(indata + [indata[-1] + 3], [0] + indata)):
        if distance == 3 or distance == 2 and current_block[-2:-1] == [2]:
            if len(current_block) > 1:
                distinct_blocks.append(current_block)
            current_block = []
        else:
            current_block.append(distance)
    num_ways_through = 1
    for block in distinct_blocks:
        distinct_ways_past = [[0, [1]]] + [[distance, [0]] for distance in block]
        for i in range(len(distinct_ways_past)):
            _, [num_ways_here] = distinct_ways_past[i]
            tolerance_left = 3
            for distance, num_ways_there_ref in distinct_ways_past[i+1:i+4]:
                if tolerance_left < distance:
                    break
                tolerance_left -= distance
                num_ways_there_ref[0] += num_ways_here
        _, [num_ways_through_block] = distinct_ways_past[-1]
        num_ways_through *= num_ways_through_block
    print("Second star: {}".format(num_ways_through))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])