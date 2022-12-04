"""
day_4.py

given a list of assignments in pairs, e.g:

    2-4, 6-8
    2-3, 4-5
    6-6, 4-6

list all the times one of the pair is completely included
by the other (e.g 2-3, 1-4, 1-4 includes 2-3).
optional: find the overlap between the two and check for enclosure that way.
"""

from dataclasses import dataclass


@dataclass
class Assignment:
    lower_bound: int
    upper_bound: int

    @property
    def assingment_size(self) -> int:
        """4-6 is size 3"""
        return self.upper_bound - self.lower_bound


def get_overlap(elf_1: Assignment, elf_2: Assignment) -> int:
    overlap_lower = max(elf_1.lower_bound, elf_2.lower_bound)
    overlap_upper = min(elf_1.upper_bound, elf_2.upper_bound)
    # sometimes there is no overlap at all: -1 will indicate this.
    overlap = max(-1, overlap_upper - overlap_lower)
    return overlap


def parse_input(input_str) -> list[list[Assignment]]:
    output = []
    for line in input_str.split("\n"):
        if not line:
            continue
        left, right = line.split(",")
        left = Assignment(*(int(x) for x in left.split("-")))
        right = Assignment(*(int(x) for x in right.split("-")))
        output.append([left, right])
    return output


def part_one(input_str: str) -> int:
    """count the pairs were one range completely encloses the other.

    we could just check with min() and max() but we will instead get the
    overlap and check if it equals the length of one pair (guessing that
    part two will need this).
    """
    redundants = 0
    assignments = parse_input(input_str)
    for assignment_1, assignment_2 in assignments:
        overlap = get_overlap(assignment_1, assignment_2)
        if overlap == min(assignment_1.assingment_size, assignment_2.assingment_size):
            redundants += 1

    return redundants


def part_two(input_str: str) -> int:
    """Return the number of pairs with non-zero overlap"""
    num_overlaps = 0
    assignments = parse_input(input_str)
    for assignment_1, assignment_2 in assignments:
        overlap = get_overlap(assignment_1, assignment_2)
        if overlap != -1:
            num_overlaps += 1
    return num_overlaps


test_input = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

assert part_one(test_input) == 2
assert part_two(test_input) == 4

if __name__ == "__main__":

    with open("input.txt") as flines:
        input_str = flines.read()

    print("part one:", part_one(input_str))
    print("part two: ", part_two(input_str))
