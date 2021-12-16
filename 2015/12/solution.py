import json
import re


def part1(input_str: str) -> int:
    regex = r"(-?\d+)"
    return sum(int(match) for match in re.findall(regex, input_str))

def part2(input_str: str) -> int:
    return count(json.loads(input_str))

def count(obj):
    if type(obj) == int:
        return obj
    elif type(obj) == list:
        return sum(count(ele) for ele in obj)
    elif type(obj) == dict:
        values = obj.values()
        if "red" in values:
            return 0
        return sum(count(ele) for ele in values)
    else:
        return 0

input_str = input()
print("part1:", part1(input_str))
print("part2:", part2(input_str))
