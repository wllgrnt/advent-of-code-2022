"""
day_5.py

given a drawing of the starting stacks of crates and the rearrangement procedure,
e.g:
----
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
----

list the crates on top of each stack at the end of the procedure - e.g CMZ
"""

from dataclasses import dataclass
from itertools import zip_longest
from string import ascii_uppercase


# overkill, but assuming this needs more functionality later.
@dataclass
class Tower:
    """A tower of crates, represented by a list (could be a queue, just needs to be LIFO)."""

    stack: list


@dataclass
class Instruction:
    """The instructions for transporting crates."""

    volume: int
    source: int
    dest: int


PuzzleInput = tuple[list[Tower], list[Instruction]]


def parse_input(input_str) -> PuzzleInput:
    crate_position_str, instruction_list_str = input_str.split("\n\n")
    # parse the crates
    crate_matrix = [line for line in crate_position_str.splitlines()]
    num_towers = (len(crate_matrix[0]) + 1) // 4
    towers = [[] for i in range(num_towers)]
    # each crate looks like [A] [D] so read the 2nd, 6th, etc chars
    for line in crate_matrix:
        for tower_num, i in enumerate(range(1, len(line), 4)):
            crate = line[i]
            if crate in ascii_uppercase:
                towers[tower_num].append(crate)
    # reverse the stacks, it makes the code cleaner and improves performances
    towers = [Tower(x[::-1]) for x in towers]

    # parse the instruction set
    # NB changing the arg order in init will blow this up, its bad design.
    instruction_list = []
    for line in instruction_list_str.splitlines():
        vals = [int(x) for x in line.split() if x.isnumeric()]
        instruction_list.append(Instruction(*vals))
    return towers, instruction_list


def process_instruction(
    tower_list: list[Tower], instruction: Instruction, move_in_batches: bool
) -> None:
    """Here we move crates one at a time."""
    vol = instruction.volume
    source_index = instruction.source - 1  # zero-based indexing
    dest_index = instruction.dest - 1
    if move_in_batches:
        crates_to_move = []
        # add to stack then reorder - could also just split the list.
        for _ in range(vol):
            crates_to_move.append(tower_list[source_index].stack.pop())
        tower_list[dest_index].stack += crates_to_move[::-1]
    else:
        for _ in range(vol):
            crate = tower_list[source_index].stack.pop()
            tower_list[dest_index].stack.append(crate)


def part_one(input_str: str) -> str:
    """
    process the crates according to the instructions, return the crates on top at the end.
    The crates are moved one by one.
    """

    tower_list, instruction_list = parse_input(input_str)

    for instruction in instruction_list:
        process_instruction(tower_list, instruction, move_in_batches=False)

    return "".join(tower.stack[-1] for tower in tower_list)


def part_two(input_str: str) -> str:
    """
    process the crates according to the instructions, return the crates on top at the end.
    The crates are moved in batches.
    """

    tower_list, instruction_list = parse_input(input_str)

    for instruction in instruction_list:
        process_instruction(tower_list, instruction, move_in_batches=True)

    return "".join(tower.stack[-1] for tower in tower_list)


test_input = """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

assert part_one(test_input) == "CMZ"
assert part_two(test_input) == "MCD"

if __name__ == "__main__":

    with open("input.txt") as flines:
        input_str = flines.read()

    print("part one:", part_one(input_str))
    print("part two: ", part_two(input_str))
