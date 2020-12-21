import collections
import enum
import functools
import io
import itertools
import math
import operator
import re
import sys

def first(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    foodstuff_regex = re.compile(r'(?P<ingredients>[a-z ]+) \(contains (?P<allergens>[a-z, ]+)\)')
    allergen_possibilities = {}
    ingredient_counts = {}
    for match in foodstuff_regex.finditer(indata):
        ingredients_set = set(match['ingredients'].strip().split(' '))
        for ingredient in ingredients_set:
            ingredient_counts.setdefault(ingredient, 0)
            ingredient_counts[ingredient] += 1
        for allergen in match['allergens'].strip().split(', '):
            if allergen in allergen_possibilities:
                allergen_possibilities[allergen] &= ingredients_set
            else:
                allergen_possibilities[allergen] = set(ingredients_set)
    non_allergenic_count = 0
    non_allergenic_ingredients = set(ingredient_counts.keys())
    for allergen, allergenic_ingredients in allergen_possibilities.items():
        non_allergenic_ingredients -= allergenic_ingredients
    for ingredient in non_allergenic_ingredients:
        non_allergenic_count += ingredient_counts[ingredient]
    print("First star: {}".format(non_allergenic_count))

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    foodstuff_regex = re.compile(r'(?P<ingredients>[a-z ]+) \(contains (?P<allergens>[a-z, ]+)\)')
    allergen_possibilities = {}
    ingredient_counts = {}
    for match in foodstuff_regex.finditer(indata):
        ingredients_set = set(match['ingredients'].strip().split(' '))
        for ingredient in ingredients_set:
            ingredient_counts.setdefault(ingredient, 0)
            ingredient_counts[ingredient] += 1
        for allergen in match['allergens'].strip().split(', '):
            if allergen in allergen_possibilities:
                allergen_possibilities[allergen] &= ingredients_set
            else:
                allergen_possibilities[allergen] = set(ingredients_set)
    resolved_allergens = {}
    while allergen_possibilities:
        for allergen, possible_ingredients in allergen_possibilities.items():
            if len(possible_ingredients) == 1:
                allergenic_ingredient = possible_ingredients.pop()
                break
        else:
            print(f"Error: {allergen_possibilities}")
        resolved_allergens[allergen] = allergenic_ingredient
        del allergen_possibilities[allergen]
        for possible_ingredients in allergen_possibilities.values():
            possible_ingredients.discard(allergenic_ingredient)
    allergens = list(resolved_allergens.keys())
    allergens.sort()
    print("Second star: {}".format(','.join((resolved_allergens[allergen] for allergen in allergens))))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])