import functools
import io
import operator
import re
import sys

def first(file_name):
    print("First star: {}".format(sum([len("".join(match)) for match in re.findall(r'(?:(?:{})\n?)+'.format('|'.join(['(?P<{0}>{0})'.format(chr(c)) for c in range(ord('a'), ord('z') + 1)])), io.open(file_name).read())])))

def second(file_name):
    print("Second star: {}".format(sum([len("".join(match)) for match in re.findall(r'(?:(?:(?:{})|.)+(?:\n.+)*)'.format('|'.join([r'(?P<{0}>{0}(?=.*(?:\n.*{0}.*)*\n(?:\n|$)))'.format(chr(c)) for c in range(ord('a'), ord('z') + 1)])), io.open(file_name).read())])))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])