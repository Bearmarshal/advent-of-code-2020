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
    regex = re.compile(r'(?:(?P<field>[a-z ]+): (?P<ranges>\d+-\d+(?: or \d+-\d+)*)|(?P<my_ticket>\d+(?:,\d+)*(?=\n+nearby tickets))|(?P<other_tickets>(\d+(?:,\d+)*(?:\n|$))*(?!\n+nearby tickets)))')
    range_regex = re.compile(r'(?P<range_start>\d+)-(?P<range_end>\d+)')
    valid_somewhere = set()
    num_invalid = 0
    invalid_values = []
    for match in regex.finditer(indata):
        if match['field']:
            for range_match in range_regex.finditer(match['ranges']):
                valid_somewhere |= set(range(int(range_match['range_start']), int(range_match['range_end']) + 1))
        if tickets := match['other_tickets']:
            other_tickets = tickets.strip().split('\n')
    for ticket in other_tickets:
        invalid_values += [value for value_string in ticket.split(',') if (value := int(value_string)) not in valid_somewhere]
    print("First star: {}".format(sum(invalid_values)))

# def second(file_name):
#     with io.open(file_name, mode = 'r') as infile:
#         indata = infile.read()
#     print("Second star: {}".format(0))

if __name__ == "__main__":
    first(sys.argv[1])
    # second(sys.argv[1])