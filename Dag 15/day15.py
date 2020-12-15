import collections
import enum
import functools
import io
import itertools
import operator
import re
import sys

def first(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    curr_number = 0
    turn = 0
    memory = {(curr_number := number): ((turn := i), 0) for i, number in enumerate(map(int, re.findall(r'\d+', indata)), 1)}
    turn += 1
    while turn <= 2020:
        when_last_said, when_said_before = memory[curr_number]
        if not when_said_before:
            curr_number = 0
        else:
            curr_number = when_last_said - when_said_before
        curr_last_said, _ = memory.get(curr_number, (0, 0))
        memory[curr_number] = turn, curr_last_said
        turn += 1
    print("First star: {}".format(curr_number))

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    curr_number = 0
    turn = 0
    memory = {(curr_number := number): ((turn := i), 0) for i, number in enumerate(map(int, re.findall(r'\d+', indata)), 1)}
    turn += 1
    while turn <= 30000000:
        when_last_said, when_said_before = memory[curr_number]
        if not when_said_before:
            curr_number = 0
        else:
            curr_number = when_last_said - when_said_before
        curr_last_said, _ = memory.get(curr_number, (0, 0))
        memory[curr_number] = turn, curr_last_said
        turn += 1
    print("Second star: {}".format(curr_number))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])