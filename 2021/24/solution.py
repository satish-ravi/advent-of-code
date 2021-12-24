import sys
from collections import defaultdict
from enum import Enum
from typing import Callable, Optional, Union

BLOCK_SIZE = 18


class Operator(Enum):
    INP = "inp"
    ADD = "add"
    MUL = "mul"
    DIV = "div"
    MOD = "mod"
    EQL = "eql"


class Registry(Enum):
    w = "w"
    x = "x"
    y = "y"
    z = "z"


class BlockType(Enum):
    ADD = 1
    DIVIDE = 2


class Instruction:
    operator: Operator
    operand1: Registry
    operand2: Optional[Union[Registry, int]]

    def __init__(self, ins_str: str):
        operator, operands = ins_str.split(" ", 1)
        self.operator = Operator(operator)
        if self.operator == Operator.INP:
            self.operand1 = Registry(operands)
            self.operand2 = None
        else:
            op1, op2 = operands.split(" ")
            self.operand1 = Registry(op1)
            try:
                self.operand2 = int(op2)
            except ValueError:
                self.operand2 = Registry(op2)

    def __repr__(self) -> str:
        return f"{self.operator.value} {self.operand1.value} {self.operand2.value if type(self.operand2) == Registry else self.operand2}"


class Block:
    block_type: BlockType
    value: int

    def __init__(self, instructions: list[Instruction]) -> None:
        assert len(instructions) == BLOCK_SIZE
        assert instructions[0].operator == Operator.INP
        assert instructions[-1].operator == Operator.ADD

        # 5th instruction identifies whether it's an ADD or a DIVIDE block
        assert instructions[4].operator == Operator.DIV
        assert instructions[4].operand1 == Registry.z
        assert instructions[4].operand2 in [1, 26]

        # Instructions of interest, 6th for divide block, 16th for add block
        assert instructions[5].operator == Operator.ADD
        assert instructions[5].operand1 == Registry.x
        assert instructions[-3].operator == Operator.ADD
        assert instructions[-3].operand1 == Registry.y

        if instructions[4].operand2 == 1:
            self.block_type = BlockType.ADD
            self.value = instructions[-3].operand2
        else:
            self.block_type = BlockType.DIVIDE
            self.value = instructions[5].operand2

    def __repr__(self) -> str:
        return f"{self.block_type.value} {self.value}"


def read_input() -> list[Instruction]:
    return [Instruction(l.strip()) for l in sys.stdin.readlines()]


def create_blocks(instructions: list[Instruction]) -> list[Block]:
    assert len(instructions) % BLOCK_SIZE == 0

    blocks = []
    for block_index in range(0, len(instructions), BLOCK_SIZE):
        blocks.append(Block(instructions[block_index : block_index + BLOCK_SIZE]))
    return blocks


def run_alu(instructions: list[Instruction], num: str) -> int:
    registries = defaultdict(int)
    inputs = (int(n) for n in num)
    for instruction in instructions:
        op = instruction.operator
        op1 = instruction.operand1
        if op == Operator.INP:
            registries[op1] = next(inputs)
        else:
            op2 = registries[instruction.operand2] if type(instruction.operand2) == Registry else instruction.operand2
            if op == Operator.ADD:
                registries[op1] += op2
            elif op == Operator.MUL:
                registries[op1] *= op2
            elif op == Operator.DIV:
                registries[op1] //= op2
            elif op == Operator.MOD:
                registries[op1] %= op2
            elif op == Operator.EQL:
                registries[op1] = 1 if registries[op1] == op2 else 0
            else:
                raise ValueError(f"invalid operator: {op}")
    return registries[Registry.z]


def solve(instructions: list[Instruction], num_fn: Callable[[int], tuple[int, int]]) -> str:
    stack = []
    deltas = []

    blocks = create_blocks(instructions)
    for index, block in enumerate(blocks):
        if block.block_type == BlockType.ADD:
            # For add blocks, value in instruction 16 + input is added to z
            stack.append((index, block.value))
        else:
            start_index, value = stack.pop()
            # For divide blocks, in order for not adding value to z, x must resolve to 0.
            # For this to happen, last add block input + last add block instruction 16 == this block input - this block instruction 6
            # Just keep track of last add block index, current index and sum of the two instruction values
            # Based on https://www.reddit.com/r/adventofcode/comments/rnejv5/2021_day_24_solutions/hps5hgw/?utm_source=reddit&utm_medium=web2x&context=3
            deltas.append((start_index, index, value + block.value))
    assert len(stack) == 0

    result_arr = [None] * (len(instructions) // BLOCK_SIZE)

    for (index1, index2, delta) in deltas:
        result_arr[index1], result_arr[index2] = num_fn(delta)

    result = "".join(str(n) for n in result_arr)
    assert run_alu(instructions, result) == 0

    return result


def part1_nums(delta: int) -> tuple[int, int]:
    return min(9, 9 - delta), min(9, 9 + delta)


def part2_nums(delta: int) -> tuple[int, int]:
    return max(1, 1 - delta), max(1, 1 + delta)


instructions = read_input()
print("part1:", solve(instructions, part1_nums))
print("part2:", solve(instructions, part2_nums))
