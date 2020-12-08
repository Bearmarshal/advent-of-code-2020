import collections
import functools
import io
import operator
import re
import sys

def first(file_name):
    pc = 0
    acc = 0
    visited = set()
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    code = [(operation, int(argument)) for operation, argument in re.findall(r'([a-z]{3}) ([+-]\d+)', indata)]
    while pc not in visited:
        visited.add(pc)
        operation, argument = code[pc]
        if operation == 'acc':
            acc += argument
            pc += 1
        elif operation == 'jmp':
            pc += argument
        elif operation == 'nop':
            pc += 1
        else:
            print('error: {}'.format(operation))
    print("First star: {}".format(acc))

def second(file_name):
    pc = 0
    acc = 0
    visited = set()
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    code = [(operation, int(argument)) for operation, argument in re.findall(r'([a-z]{3}) ([+-]\d+)', indata)]
    while pc not in visited:
        visited.add(pc)
        operation, argument = code[pc]
        if operation == 'acc':
            pc += 1
        elif operation == 'jmp':
            pc += argument
        elif operation == 'nop':
            pc += 1
        else:
            print('error: {}'.format(operation))
    terminating = set()
    non_terminating = set(visited)
    for start_pc in range(len(code)):
        if start_pc in non_terminating or start_pc in terminating:
            continue
        curr_visited = set()
        curr_pc = start_pc
        while curr_pc in range(len(code)):
            if curr_pc in curr_visited or curr_pc in non_terminating:
                non_terminating |= curr_visited
                break
            curr_visited.add(curr_pc)
            operation, argument = code[curr_pc]
            if operation == 'acc':
                curr_pc += 1
            elif operation == 'jmp':
                curr_pc += argument
            elif operation == 'nop':
                curr_pc += 1
            else:
                print('error: {}'.format(operation))
        else:
            terminating |= curr_visited
    for pc in visited:
        operation, argument = code[pc]
        if operation == 'nop' and pc + argument in terminating:
            code[pc] = ('jmp', argument)
            break
        elif operation == 'jmp' and pc + 1 in terminating:
            code[pc] = ('nop', argument)
            break
    pc = 0
    while pc in range(len(code)):
        visited.add(pc)
        operation, argument = code[pc]
        if operation == 'acc':
            acc += argument
            pc += 1
        elif operation == 'jmp':
            pc += argument
        elif operation == 'nop':
            pc += 1
        else:
            print('error: {}'.format(operation))
    print("Second star: {}".format(acc))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])