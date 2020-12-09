import collections
import functools
import io
import operator
import re
import sys

def first(file_name):
    previous = collections.deque()
    matching_numbers = {}
    with io.open(file_name, mode = 'r') as infile:
        for line in infile:
            number = int(line)
            if len(previous) == 25:
                if number not in matching_numbers:
                    break
                else:
                    oldest = previous.popleft()
                    for other_number in previous:
                        sum = oldest + other_number
                        if matching_numbers[sum] == 1:
                            del(matching_numbers[sum])
                        else:
                            matching_numbers[sum] -= 1
            for other_number in previous:
                sum = number + other_number
                if sum not in matching_numbers:
                    matching_numbers[sum] = 0
                matching_numbers[sum] += 1
            previous.append(number)
    print("First star: {}".format(number))

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = [int(line) for line in infile]
    previous = collections.deque()
    matching_numbers = {}
    for number in indata:
        if len(previous) == 25:
            if number not in matching_numbers:
                break
            else:
                oldest = previous.popleft()
                for other_number in previous:
                    sum = oldest + other_number
                    if matching_numbers[sum] == 1:
                        del(matching_numbers[sum])
                    else:
                        matching_numbers[sum] -= 1
        for other_number in previous:
            sum = number + other_number
            if sum not in matching_numbers:
                matching_numbers[sum] = 0
            matching_numbers[sum] += 1
        previous.append(number)
    start_i = 0
    end_i = 0
    sum = 0
    while sum != number:
        if sum < number:
            sum += indata[end_i]
            end_i += 1
        else:
            sum -= indata[start_i]
            start_i += 1
    else:
        print("Second star: {}".format(min(indata[start_i:end_i]) + max(indata[start_i:end_i])))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])