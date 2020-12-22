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
    player_regex = re.compile(r'Player (?P<player>\d+):(?P<cards>(?:\n\d+)+)')
    player_decks = {}
    for match in player_regex.finditer(indata):
        player = match['player']
        deck = collections.deque()
        for card in match['cards'].strip().split('\n'):
            deck.append(int(card))
        player_decks[player] = deck
    player_1_deck = player_decks['1']
    player_2_deck = player_decks['2']
    while player_1_deck and player_2_deck:
        player_1_card = player_1_deck.popleft()
        player_2_card = player_2_deck.popleft()
        if player_1_card > player_2_card:
            player_1_deck.extend((player_1_card, player_2_card))
        else:
            player_2_deck.extend((player_2_card, player_1_card))
    winning_deck = player_1_deck if player_1_deck else player_2_deck
    print("First star: {}".format(sum((i * card for i, card in enumerate(reversed(winning_deck), 1)))))

def deck_score(deck):
    return sum((i * card for i, card in enumerate(reversed(deck), 1)))

def sub_game(player_1_deck, player_2_deck):
    state_cache = set()
    while player_1_deck and player_2_deck:
        state = player_1_deck, player_2_deck
        if state in state_cache:
            return player_1_deck, None
        state_cache.add(state)
        player_1_card = player_1_deck[0]
        player_1_deck = player_1_deck[1:]
        player_2_card = player_2_deck[0]
        player_2_deck = player_2_deck[1:]
        if player_1_card > len(player_1_deck) or player_2_card > len(player_2_deck):
            if player_1_card > player_2_card:
                player_1_deck = (*player_1_deck, player_1_card, player_2_card)
            else:
                player_2_deck = (*player_2_deck, player_2_card, player_1_card)
        else:
            player_1_sub_deck, _ = sub_game(player_1_deck[:player_1_card], player_2_deck[:player_2_card])
            if player_1_sub_deck:
                player_1_deck = (*player_1_deck, player_1_card, player_2_card)
            else:
                player_2_deck = (*player_2_deck, player_2_card, player_1_card)
    return player_1_deck, player_2_deck

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    player_regex = re.compile(r'Player (?P<player>\d+):(?P<cards>(?:\n\d+)+)')
    player_decks = {}
    for match in player_regex.finditer(indata):
        player = match['player']
        deck = []
        for card in match['cards'].strip().split('\n'):
            deck.append(int(card))
        player_decks[player] = deck
    player_1_deck, player_2_deck = sub_game(tuple(player_decks['1']), tuple(player_decks['2']))
    winning_deck = player_1_deck if player_1_deck else player_2_deck
    print("Second star: {}".format(deck_score(winning_deck)))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])