import sys
import re

inp = list(l.strip() for l in sys.stdin.readlines())

def get_first_and_last_digit(input_string):
    # Use regular expression to find all digits in the string
    digits = re.findall(r'\d', input_string)

    # Return the first and last digit as integers
    return int(digits[0]) if digits else None, int(digits[-1]) if digits else None

def get_first_and_last_digit_with_words(input_string):
    # Use regular expression to find all digits (numeric or spelled out) in the string
    digit_matches = re.findall(r'(?=(zero|one|two|three|four|five|six|seven|eight|nine|\d))', input_string)

    # Convert the matched digits to integers
    digits = [int(match) if match.isdigit() else ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"].index(match) for match in digit_matches]

    # Return the first and last digit as integers
    return digits[0] if digits else None, digits[-1] if digits else None

def solve(lines, get_first_and_last_digit_fn):
    return sum(f * 10 + l for f, l in (get_first_and_last_digit_fn(line) for line in lines))

print('part1:', solve(inp, get_first_and_last_digit))
print('part2:', solve(inp, get_first_and_last_digit_with_words))
