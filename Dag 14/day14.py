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
    or_mask = 0
    and_mask = 2 ** 36 - 1
    mem = {}
    for match in re.finditer(r'(?:mask = (?P<mask>[01X]{36})|mem\[(?P<address>\d+)\] = (?P<value>\d+))', indata):
        if mask := match['mask']:
            or_mask = int(mask.replace('X', '0'), 2)
            and_mask = int(mask.replace('X', '1'), 2)
        else:
            address = int(match['address'])
            value = int(match['value'])
            mem[address] = (value | or_mask) & and_mask
    print("First star: {}".format(sum(mem.values())))

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    or_mask = 0
    quant_mask = []
    mem = {}
    for match in re.finditer(r'(?:mask = (?P<mask>[01X]{36})|mem\[(?P<address>\d+)\] = (?P<value>\d+))', indata):
        if mask := match['mask']:
            or_mask = int(mask.replace('X', '0'), 2)
            quant_mask = [2 ** i for bit, i in zip(reversed(mask), itertools.count(0)) if bit == 'X']
        else:
            address = int(match['address']) | or_mask
            value = int(match['value'])
            for collapsed_state in itertools.product([0,1], repeat = len(quant_mask)):
                xor_mask = sum(itertools.compress(quant_mask, collapsed_state))
                mem[address ^ xor_mask] = value
    print("Second star: {}".format(sum(mem.values())))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])