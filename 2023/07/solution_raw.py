import sys
import re

inp = list(l.strip().split(' ') for l in sys.stdin.readlines())

def get_kind(hand):
    card_count = {}
    for card in hand:
        card_count[card] = card_count.get(card, 0) + 1
    if len(card_count) == 1:
        return 7
    if len(card_count) == 2:
        if 4 in card_count.values():
            return 6
        else:
            return 5
    if len(card_count) == 3:
        if 3 in card_count.values():
            return 4
        else:
            return 3
    if len(card_count) == 4:
        return 2
    return 1

def get_kind_with_joker(hand):
    card_count = {}
    for card in hand:
        card_count[card] = card_count.get(card, 0) + 1
    if len(card_count) == 1:
        return 7
    if len(card_count) == 2:
        if 4 in card_count.values():
            return 7 if card_count.get('J') in [1, 4] else 6
        else:
            return 7 if card_count.get('J') in [2, 3] else 5
    if len(card_count) == 3:
        if 3 in card_count.values():
            return 6 if card_count.get('J') in [1, 3] else 4
        else:
            return 6 if card_count.get('J') == 2 else 5 if card_count.get('J') == 1 else 3
    if len(card_count) == 4:
        return 4 if 'J' in card_count else 2
    return 2 if 'J' in card_count else 1

def map_card(card, with_joker = False):
    mapper = {'A': 'Z', 'K': 'Y', 'Q': 'X', 'J': '0' if with_joker else 'W'}
    return mapper.get(card, card)

def map_hand(hand, with_joker = False):
    return ''.join(map_card(card, with_joker) for card in hand)

sorted_hands = sorted(inp, key=lambda x: f'{get_kind(x[0])}{map_hand(x[0])}')

ans = 0
for r, hand in enumerate(sorted_hands):
    ans += (r+1) * int(hand[1])
print(ans)

sorted_hands_with_joker = sorted(inp, key=lambda x: f'{get_kind_with_joker(x[0])}{map_hand(x[0], True)}')

print(get_kind_with_joker('JQK12'))

ans = 0
for r, hand in enumerate(sorted_hands_with_joker):
    ans += (r+1) * int(hand[1])
print(ans)
