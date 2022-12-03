"""
day_3.py
each line of input represents a rucksack.
each rucksack has two compartments with equal numbers of items.
all items of a given type go in the same compartment.
each item is a single letter.
"""
from dataclasses import dataclass


# map from char to number
letter_to_score = {chr(x): i + 1 for i, x in enumerate(range(ord("a"), ord("z") + 1))}
letter_to_score |= {chr(x): i + 27 for i, x in enumerate(range(ord("A"), ord("Z") + 1))}


@dataclass
class RuckSack:
    raw_input: str
    compartment_one: str
    compartment_two: str

    def __post__init__(self):
        assert len(self.compartment_one) == len(self.compartment_two)
        assert self.compartment_one + self.compartment_two == self.raw_input

    def get_common_letters(self):
        common_letters = set()
        for item in self.compartment_one:
            if item in self.compartment_two:
                common_letters.add(item)
        return common_letters


def parse_input(input_str: str) -> list[RuckSack]:
    rucksacks = []
    for line in input_str.split("\n"):
        if not line:
            continue
        rucksacks.append(
            RuckSack(
                raw_input=line,
                compartment_one=line[: len(line) // 2],
                compartment_two=line[len(line) // 2 :],
            )
        )
    return rucksacks


def part_one(input_str: str) -> int:
    """find common items to both compartments, and score based on ordinal value.

    i.e: a-z = 1-26, A-Z = 27-52
    """

    rucksacks = parse_input(input_str)

    score = 0
    for rucksack in rucksacks:
        score += sum(letter_to_score[x] for x in rucksack.get_common_letters())
    return score


def part_two(input_str: str) -> int:
    """
    Look at groups of three rucksacks, and find the item (char) common to all three.
    """

    rucksacks = parse_input(input_str)

    assert len(rucksacks) % 3 == 0
    score = 0
    for i in range(0, len(rucksacks), 3):
        all_group_items = [x.raw_input for x in rucksacks[i: i + 3]]
        for item in all_group_items[0]:
            if item in all_group_items[1] and item in all_group_items[2]:
                # there is only one item common to all three
                badge = item
                break
        score += letter_to_score[badge]
    return score


test_input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

assert part_one(test_input) == 157

assert part_two(test_input) == 70


if __name__ == "__main__":

    with open("input.txt") as flines:
        input_str = flines.read()

    print("part one:", part_one(input_str))
    print("part two: ", part_two(input_str))
