import functools
import io
import operator
import re
import sys

def first(file_name):
    regex = re.compile(r'((((?P<byr>byr)|(?P<iyr>iyr)|(?P<eyr>eyr)|(?P<hgt>hgt)|(?P<hcl>hcl)|(?P<ecl>ecl)|(?P<pid>pid)|(?P<cid>cid)):\S+)(\s|\n))+')
    num_valid = 0
    with io.open(file_name, mode = 'r') as infile:
        batch = infile.read()
    for match in regex.finditer(batch):
        if not [True for field in ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid') if match[field] == None]:
            num_valid += 1
    print("First star: {}".format(num_valid))

def second(file_name):
    regex = re.compile(r'((byr:(?P<byr>\d{4})|iyr:(?P<iyr>\d{4})|eyr:(?P<eyr>\d{4})|hgt:(?P<hgt>(?P<hgt_cm>\d{3})cm|(?P<hgt_in>\d{2,3})in)|hcl:(?P<hcl>#[0-9a-f]{6})|ecl:(?P<ecl>amb|blu|brn|gry|grn|hzl|oth)|pid:(?P<pid>\d{9})|cid:(?P<cid>\S+))(\s|\n))+')
    num_valid = 0
    byr_range = range(1920, 2002 + 1)
    iyr_range = range(2010, 2020 + 1)
    eyr_range = range(2020, 2030 + 1)
    hgt_cm_range = range(150, 193 + 1)
    hgt_in_range = range(59, 76 + 1)
    with io.open(file_name, mode = 'r') as infile:
        batch = infile.read()
    for match in regex.finditer(batch):
        if not [True for field in ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid') if match[field] == None]:
            if int(match['byr']) in byr_range and int(match['iyr']) in iyr_range and int(match['eyr']) in eyr_range and (match['hgt_cm'] and int(match['hgt_cm']) in hgt_cm_range or match['hgt_in'] and int(match['hgt_in']) in hgt_in_range):
                num_valid += 1
    print("Second star: {}".format(num_valid))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])