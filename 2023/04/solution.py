import sys
from dataclasses import dataclass

inp = list(l.strip() for l in sys.stdin.readlines())

@dataclass
class Card:
    id: int
    winning_numbers: set[int]
    numbers: set[int]

    @property
    def my_winning_numbers(self):
        return self.numbers.intersection(self.winning_numbers)

def split_line(numbers_str):
    return set(int(n.strip()) for n in numbers_str.split(' ') if n)

def parse_input(inp):
    cards = []
    for r, row in enumerate(inp):
        winning, mine = row.split(': ')[1].split(' | ')
        cards.append(Card(r+1, split_line(winning), split_line(mine)))
    return cards

def part1(cards):
    return sum(2 ** (len(card.my_winning_numbers) - 1) for card in cards if card.my_winning_numbers)

def part2(cards):
    card_count = {card.id: 1 for card in cards}
    for card in cards:
        for copy_card_id in range(card.id + 1, card.id + 1 + len(card.my_winning_numbers)):
            card_count[copy_card_id] += card_count[card.id]
    return sum(card_count.values())

cards = parse_input(inp)

print('part1:', part1(cards))
print('part2:', part2(cards))
