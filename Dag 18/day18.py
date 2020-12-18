import collections
import functools
import io
import itertools
import operator as op
import re
import sys

def calculate(tokens):
    result = []
    operator = [None]
    for token in tokens:
        # print(token)
        (number_token, operator_token, parenthesis_token) = token
        if number_token:
            number = int(number_token)
            if operator[-1]:
                result[-1] = operator[-1](result[-1], number)
                operator[-1] = None
            else:
                result.append(number)
        elif operator_token:
            if operator_token == '+':
                operator[-1] = op.add
            elif operator_token == '*':
                operator[-1] = op.mul
        elif parenthesis_token:
            if parenthesis_token == '(':
                operator.append(None)
            elif parenthesis_token == ')':
                operator.pop()
                subexpression_result = result.pop()
                if operator[-1]:
                    result[-1] = operator[-1](result[-1], subexpression_result)
                    operator[-1] = None
                else:
                    result.append(subexpression_result)
    if len(result) != 1:
        print(f"Bad result: {result}")
    return result[0]

def first(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = [line.strip() for line in infile]
    token_regex = re.compile(r'(?P<number>\d+)|(?P<operator>[+*])|(?P<parenthesis>[()])')
    print("First star: {}".format(sum((calculate(token_regex.findall(line)) for line in indata))))

# def second(file_name):
#     with io.open(file_name, mode = 'r') as infile:
#         indata = [line.strip() for line in infile]
#     print("Second star: {}".format())

if __name__ == "__main__":
    first(sys.argv[1])
    # second(sys.argv[1])