import collections
import enum
import functools
import io
import itertools
import operator
import re
import sys

def check_can_only_be_in_one_place_recursively(field, possible_field_positions, fields_in_order):
    possible_positions = possible_field_positions[field]
    if len(possible_positions) == 1:
        position = possible_positions.pop()
        print(f"{field} must be at position {position}")
        fields_in_order[position] = field
        del possible_field_positions[field]
        for other_field, other_possible_positions in list(possible_field_positions.items()):
            if position in other_possible_positions:
                other_possible_positions.remove(position)
                check_can_only_be_in_one_place_recursively(other_field, possible_field_positions, fields_in_order)

class Possibilities:
    def __init__(self, fields):
        self.positions = {field: set(range(len(fields))) for field in fields}
        self.fields = {position: set(fields) for position in range(len(fields))}
        self.resolved = {}

    def exclude(self, field, position):
        if field in self.positions and position in self.positions[field]:
            self.meticulous_exclude(field, position)
        
    def meticulous_exclude(self, field, position):
        if field in self.positions:
            possible_positions = self.positions[field]
            if position in possible_positions:
                possible_positions.remove(position)
                if len(possible_positions) == 1:
                    position_of_field = possible_positions.pop()
                    self.positions.pop(field, None)
                    self.fields.pop(position_of_field, None)
                    self.resolved[field] = position_of_field
                    for other_field in list(self.positions):
                        self.meticulous_exclude(other_field, position_of_field)
        if position in self.fields:
            possible_fields = self.fields[position]
            if field in possible_fields:
                possible_fields.remove(field)
                if len(possible_fields) == 1:
                    field_at_position = possible_fields.pop()
                    self.positions.pop(field_at_position, None)
                    self.fields.pop(position, None)
                    self.resolved[field_at_position] = position
                    for other_position in list(self.fields):
                        self.meticulous_exclude(field, other_position)

    def are_resolved(self):
        return not self.positions

def first(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    regex = re.compile(r'(?:(?P<field>[a-z ]+): (?P<ranges>\d+-\d+(?: or \d+-\d+)*)|(?P<my_ticket>\d+(?:,\d+)*(?=\n+nearby tickets))|(?P<other_tickets>(\d+(?:,\d+)*(?:\n|$))*(?!\n+nearby tickets)))')
    range_regex = re.compile(r'(?P<range_start>\d+)-(?P<range_end>\d+)')
    valid_somewhere = set()
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

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    field_data, ticket_data = indata.split("your ticket:")
    fields = {}
    for field_match in re.finditer(r'(?:(?P<field>[a-z ]+): (?P<ranges>\d+-\d+(?: or \d+-\d+)*))', field_data):
        field = field_match['field']
        fields[field] = set()
        for range_match in re.finditer(r'(?P<range_start>\d+)-(?P<range_end>\d+)', field_match['ranges']):
            fields[field] |= set(range(int(range_match['range_start']), int(range_match['range_end']) + 1))
    valid_somewhere = functools.reduce(operator.or_, fields.values())
    possibilities = Possibilities(fields)
    my_ticket_data, other_tickets_data = ticket_data.split("nearby tickets:")
    my_ticket = list(map(int, my_ticket_data.strip().split(',')))
    for other_ticket_data in other_tickets_data.strip().split('\n'):
        other_ticket = list(map(int, other_ticket_data.strip().split(',')))
        if not set(other_ticket) - valid_somewhere:
            for position, value in enumerate(list(other_ticket)):
                for field, possible_positions in list(possibilities.positions.items()):
                    if position in possible_positions and value not in fields[field]:
                        possibilities.exclude(field, position)
        if possibilities.are_resolved():
            print("Second star: {}".format(functools.reduce(operator.mul, [my_ticket[possibilities.resolved[field]] for field in fields if "departure" in field])))
            break
    else:
        print(f"Inconclusive: {possibilities.positions}")

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])