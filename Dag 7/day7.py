import collections
import functools
import io
import operator
import re
import sys

def first(file_name):
    containing_bags = dict()
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    for rule in re.findall(r'(\w+ \w+) bags contain ([^.]+)\.', indata):
        for contained_bag in re.findall(r'\d+ (\w+ \w+) bag', rule[1]):
            if contained_bag not in containing_bags:
                containing_bags[contained_bag] = []
            containing_bags[contained_bag] += [rule[0]]
    can_contain_shiny_gold = set(containing_bags['shiny gold'])
    to_check = collections.deque(can_contain_shiny_gold)
    while len(to_check):
        bag = to_check.popleft()
        if bag in containing_bags:
            for containing_bag in containing_bags[bag]:
                if containing_bag not in can_contain_shiny_gold:
                    can_contain_shiny_gold.add(containing_bag)
                    to_check.append(containing_bag)
    print("First star: {}".format(len(can_contain_shiny_gold)))

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    bag_contents = {bag: {contained_bag: int(number_of) for number_of, contained_bag in re.findall(r'(\d+) (\w+ \w+) bag', contents)} for bag, contents in re.findall(r'(\w+ \w+) bags contain ([^.]+)\.', indata)}
    to_count = bag_contents['shiny gold']
    num_bags_in_shiny_gold = 0
    while len(to_count):
        contained_bag, number_of = to_count.popitem()
        num_bags_in_shiny_gold += number_of
        if contained_bag in bag_contents:
            for inner_bag, inner_number_of in bag_contents[contained_bag].items():
                if inner_bag not in to_count:
                    to_count[inner_bag] = 0
                to_count[inner_bag] += number_of * inner_number_of
    print("Second star: {}".format(num_bags_in_shiny_gold))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])