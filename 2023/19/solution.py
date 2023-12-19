import sys
from dataclasses import dataclass

inp = list(l.strip() for l in sys.stdin.readlines())

@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def get_value(self, category):
        if category == 'x':
            return self.x
        if category == 'm':
            return self.m
        if category == 'a':
            return self.a
        if category == 's':
            return self.s

    def set_value(self, category, value):
        if category == 'x':
            self.x = value
        elif category == 'm':
            self.m = value
        elif category == 'a':
            self.a = value
        elif category == 's':
            self.s = value

    @property
    def total_rating(self):
        return self.x + self.m + self.a + self.s

    def clone(self):
        return Part(self.x, self.m, self.a, self.s)

@dataclass
class PartRange:
    start: Part
    end: Part

    def is_valid(self):
        return all(self.start.get_value(category) <= self.end.get_value(category) for category in 'xmas')

    @property
    def total_parts(self):
        total = 1
        for category in 'xmas':
            total *= self.end.get_value(category) - self.start.get_value(category) + 1
        return total

    def clone(self):
        return PartRange(self.start.clone(), self.end.clone())

@dataclass
class Rule:
    category: str
    operator: str
    cmp_value: int
    result: str

    def matches(self, part):
        value = part.get_value(self.category)
        return value > self.cmp_value if self.operator == '>' else value < self.cmp_value

    def split_range(self, part_range):
        matching = part_range.clone()
        non_matching = part_range.clone()
        if self.operator == '<':
            matching.end.set_value(self.category, self.cmp_value - 1)
            non_matching.start.set_value(self.category, self.cmp_value)
        else:
            matching.start.set_value(self.category, self.cmp_value + 1)
            non_matching.end.set_value(self.category, self.cmp_value)
        return matching, non_matching

@dataclass
class Workflow:
    name: str
    rules: list[Rule]
    fallback: str

    def get_output(self, part):
        for rule in self.rules:
            if rule.matches(part):
                return rule.result
        return self.fallback

    def get_output_range(self, part_range):
        current = part_range
        result = []
        for rule in self.rules:
            matching, non_matching = rule.split_range(current)
            result.append((matching, rule.result))
            current = non_matching
        result.append((current, self.fallback))
        return result

def parse_input(inp):
    workflows = {}
    parts = []

    finished_wfs = False
    for row in inp:
        if row == '':
            finished_wfs = True
            continue
        if finished_wfs:
            x, m, a, s = [int(element.split('=')[1]) for element in row[1:-1].split(',')]
            parts.append(Part(x, m, a, s))
        else:
            wf_name, raw_rules = row[:-1].split('{')
            rules_split = raw_rules.split(',')
            rules = []
            for raw_rule in rules_split[:-1]:
                condition, result = raw_rule.split(':')
                category = condition[0]
                operator = condition[1]
                cmp_value = int(condition[2:])
                rules.append(Rule(category, operator, cmp_value, result))
            workflows[wf_name] = Workflow(wf_name, rules, rules_split[-1])
    return workflows, parts

def part1(workflows, parts):
    result = 0
    for part in parts:
        workflow = 'in'
        while workflow not in {'A', 'R'}:
            workflow = workflows[workflow].get_output(part)
        if workflow == 'A':
            result += part.total_rating
    return result

def part2(workflows):
    result = 0
    start_range = PartRange(Part(1,1,1,1), Part(4000,4000,4000,4000))
    stack = [(start_range, 'in')]

    while stack:
        current_range, wf_name = stack.pop()

        if not current_range.is_valid:
            continue
        if wf_name == 'R':
            continue
        if wf_name == 'A':
            result += current_range.total_parts
            continue
        stack.extend(workflows[wf_name].get_output_range(current_range))

    return result

workflows, parts = parse_input(inp)

print('part1:', part1(workflows, parts))
print('part2:', part2(workflows))
