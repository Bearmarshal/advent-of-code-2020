import io
import re
import sys

def first(file_name):
    regex = re.compile(r'(\d+)-(\d+) ([a-z]): ([a-z]+)')
    num_valid = 0
    with io.open(file_name, mode = 'r') as infile:
        for line in infile:
            line_match = regex.match(line)
            min_occurences = int(line_match[1])
            max_occerences = int(line_match[2])
            character = line_match[3]
            password = line_match[4]
            num_occurences = password.count(character)
            if num_occurences in range(min_occurences, max_occerences + 1):
                num_valid += 1
    print("First star: {}".format(num_valid))

def second(file_name):
    regex = re.compile(r'(\d+)-(\d+) ([a-z]): ([a-z]+)')
    num_valid = 0
    with io.open(file_name, mode = 'r') as infile:
        for line in infile:
            line_match = regex.match(line)
            first_position = int(line_match[1]) - 1
            second_position = int(line_match[2]) - 1
            character = line_match[3]
            password = line_match[4]
            num_occurences = password[first_position].count(character) + password[second_position].count(character)
            if num_occurences == 1:
                num_valid += 1
    print("Second star: {}".format(num_valid))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])