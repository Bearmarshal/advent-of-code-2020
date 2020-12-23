import collections
import enum
import functools
import io
import itertools
import math
import operator
import re
import sys

class Cup:
    def __init__(self, label, previous = None):
        self.label = label
        self.next = None
        if previous:
            previous.next = self

    def str_join(self, n, separator = '', ):
        string = str(self.label)
        next = self.next
        for _ in range(1, n):
            string += separator + str(next.label)
            next = next.next
        return string

def move(cups, current_label, highest_label, lowest_label):
    current_cup = cups[current_label]
    moving_labels = (first_moving_cup := current_cup.next).label, (next := first_moving_cup.next).label, (last_moving_cup := next.next).label
    destination_label = current_label - 1 if current_label != lowest_label else highest_label
    while destination_label in moving_labels:
        destination_label = destination_label - 1 if destination_label != lowest_label else highest_label
    destination_cup = cups[destination_label]
    current_cup.next = last_moving_cup.next
    last_moving_cup.next = destination_cup.next
    destination_cup.next = first_moving_cup
    return current_cup.next.label

def first(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    cups = [None] * (len(indata) + 1)
    first = None
    cup = None
    highest_label = math.nan
    lowest_label = math.nan
    for label_digit in indata:
        label = int(label_digit)
        cup = Cup(label, cup)
        cups[label] = cup
        highest_label = highest_label if highest_label > label else label
        lowest_label = lowest_label if lowest_label < label else label
        if not first:
            first = cup
    cup.next = first
    current_label = first.label
    for _ in range(100):
        current_label = move(cups, current_label, highest_label, lowest_label)
    result = cups[1].next.str_join(highest_label - lowest_label)
    print("First star: {}".format(result))

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    cups = [None] * (1_000_000 + 1)
    first = None
    cup = None
    highest_label = math.nan
    lowest_label = math.nan
    for label_digit in indata:
        label = int(label_digit)
        cup = Cup(label, cup)
        cups[label] = cup
        highest_label = highest_label if highest_label > label else label
        lowest_label = lowest_label if lowest_label < label else label
        if not first:
            first = cup
    for label in range(highest_label + 1, 1_000_000 + 1):
        cup = Cup(label, cup)
        cups[label] = cup
    cup.next = first
    highest_label = 1_000_000
    current_label = first.label
    for _ in range(10_000_000):
        current_label = move(cups, current_label, highest_label, lowest_label)
    result = cups[1].next.label * cups[1].next.next.label
    print("Second star: {}".format(result))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])