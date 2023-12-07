import sys
from dataclasses import dataclass

inp = list(l.strip() for l in sys.stdin.readlines())

@dataclass
class Hand:
    hand: str
    bid: int

    def get_kind(self):
        card_count = {}
        for card in self.hand:
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


    def get_kind_with_joker(self):
        card_count = {}
        for card in self.hand:
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

    def serialize(self, with_joker):
        mapper = {'A': 'Z', 'K': 'Y', 'Q': 'X', 'J': '0' if with_joker else 'W'}
        kind = self.get_kind_with_joker() if with_joker else self.get_kind()
        return f'{kind}{"".join(mapper.get(card, card) for card in self.hand)}'

def parse_input(inp):
    hands = []
    for line in inp:
        hand, bid_str = line.split(' ')
        hands.append(Hand(hand, int(bid_str)))
    return hands

def solve(hands, with_joker):
    result = 0
    sorted_hands = sorted(hands, key=lambda hand: hand.serialize(with_joker))
    for i, hand in enumerate(sorted_hands):
        result += (i + 1) * hand.bid
    return result

hands = parse_input(inp)
print('part1:', solve(hands, False))
print('part2:', solve(hands, True))