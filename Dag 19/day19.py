import collections
import enum
import functools
import io
import itertools
import operator
import re
import sys

def resolve_references(rule_id, rule_data_map, resolved_rules_map = {}):
    if rule_id in resolved_rules_map:
        return resolved_rules_map[rule_id]
    rule_parts = rule_data_map[rule_id]
    resolved_rule = ""
    has_pipe = False
    for part in rule_parts:
        if string := part['string']:
            resolved_rule += string
        elif referenced_id := part['reference']:
            resolved_rule += resolve_references(referenced_id, rule_data_map, resolved_rules_map)
        elif part['pipe']:
            resolved_rule += '|'
            has_pipe = True
    if has_pipe:
        resolved_rule = '(?:' + resolved_rule + ')'
    resolved_rules_map[rule_id] = resolved_rule
    return resolved_rule

def first(file_name):
    rule_regex = re.compile(r'"(?P<string>[a-z]+)"|(?P<reference>\d+)|(?P<pipe>\|)')
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    rule_data, message_data = indata.split('\n\n')
    rule_data_map = {}
    for rule_id, single_rule_data in map(lambda row: row.split(':'), rule_data.strip().split('\n')):
        rule_data_map[rule_id] = [match for match in rule_regex.finditer(single_rule_data)]
    message_regex = re.compile('(?m)^' + resolve_references('0', rule_data_map) + '$')
    print("First star: {}".format(len(list(message_regex.finditer(message_data)))))

def rule0_match(rule42, rule31, string):
    if match := re.search('^' + rule42 + '(?P<inner>.*)' + rule31 + '$', string):
        if inner := match['inner']:
            return rule0_match(rule42, rule31, inner) or re.match('^' + rule42 + '+$', inner)
        else:
            return False
    else:
        return False

def second(file_name):
    rule_regex = re.compile(r'"(?P<string>[a-z]+)"|(?P<reference>\d+)|(?P<pipe>\|)')
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    rule_data, message_data = indata.split('\n\n')
    rule_data_map = {}
    for rule_id, single_rule_data in map(lambda row: row.split(':'), rule_data.strip().split('\n')):
        rule_data_map[rule_id] = [match for match in rule_regex.finditer(single_rule_data)]
    resolved_rules_map = {}
    rule42 = resolve_references('42', rule_data_map, resolved_rules_map)
    rule31 = resolve_references('31', rule_data_map, resolved_rules_map)
    matching_messages = [message for message in message_data.split('\n') if rule0_match(rule42, rule31, message)]
    print("Second star: {}".format(len(matching_messages)))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])