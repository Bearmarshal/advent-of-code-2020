import collections
import functools
import io
import operator
import re
import sys

def first(file_name):
    previous = []
    matching_numbers = {}
    i = 0
    with io.open(file_name, mode = 'r') as infile:
        for line in infile:
            number = int(infile.readline())
            for other_number in previous:
                sum = number + other_number
                if sum not in matching_numbers:
                    matching_numbers[sum] = 0
                matching_numbers[sum] += 1
            previous += [number]
        matching_numbers = {a + b: (a, b) for a in previous for b in previous if a != b}
        for line in infile:
            number = int(line)
            if number not in matching_numbers:
                print("First star: {}".format(number))
                break
            else:
                print("{} = {} + {}".format(number, matching_numbers[number][0], matching_numbers[number][1]))

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    print("Second star: {}".format(acc))

if __name__ == "__main__":
    first(sys.argv[1])
    #second(sys.argv[1])