"""
day_11.py

Monkey Business:

We get a set of rules for each monkey - it inspects its items, in order, and then
throws them depending on the condition. Each monkey goes in order - this makes up one
round.
Part one - find the total number of inspections each monkey performs after 20 rounds. Return the multiple
of the two highest values.
"""
import re

from typing import Callable
from collections import deque
from math import prod

NUMBER_OF_ROUNDS = 20
WORRY_REDUCTION = 3


class Monkey:
    def __init__(
        self,
        items: deque[int],
        operation: Callable,
        divisor: int,
        monkey_if_true: int,
        monkey_if_false: int,
    ) -> None:
        """
        Args:
            items: the items held
            operation: a function that takes an int and returns an int.
            divisor: the divisor used to test the item
            monkey_if_true: an integer index for a monkey
            monkey_if_false: an integer index for a monkey
        """
        self.items = items
        self.operation = operation
        self.divisor = divisor
        self.monkey_if_true = monkey_if_true
        self.monkey_if_false = monkey_if_false
        self.number_of_inspections = 0

    def __repr__(self) -> str:
        """useful for debugging"""
        return f"Monkey(items={self.items}, operation={self.operation}, divisor={self.divisor}, monkey_if_true={self.monkey_if_true}, monkey_if_false={self.monkey_if_false})"

    @classmethod
    def from_text(cls, input_str: str):
        # drop the index line
        (
            _,
            items_line,
            operation,
            test,
            test_if_true,
            test_if_false,
        ) = input_str.splitlines()
        # gross parsing
        item_list = [int(x) for x in re.findall(r"\d+", items_line)]
        operation_lambda = lambda old: eval(operation.split("=")[-1])  # noqa
        divisor = int(test.split()[-1])
        monkey_if_true = int(test_if_true.split()[-1])
        monkey_if_false = int(test_if_false.split()[-1])
        return cls(
            deque(item_list), operation_lambda, divisor, monkey_if_true, monkey_if_false
        )


def generate_monkey_list(input_str: str) -> list[Monkey]:
    """Parse the input string into a list of Monkeys."""
    monkeys = []
    for monkey_text in input_str.split("\n\n"):
        monkeys.append(Monkey.from_text(monkey_text))
    return monkeys


def monkey_business(monkey_list: list[Monkey], worry_reduction, max_worry):
    """Each monkey inspects its items in order, and then tests them and throws them

    TODO: should not be iteracting with these attributes directly.
    ."""
    for monkey in monkey_list:
        while monkey.items:
            item = monkey.items.popleft()
            new_item = monkey.operation(item) // worry_reduction % max_worry
            if new_item % monkey.divisor == 0:
                monkey_list[monkey.monkey_if_true].items.append(new_item)
            else:
                monkey_list[monkey.monkey_if_false].items.append(new_item)
            monkey.number_of_inspections += 1


def part_one(input_str: str, number_of_rounds=20, worry_reduction=3) -> int:
    """Find the total number of inspections each monkey performs after 20 rounds.

    Returns:
        the multiple of the two highest values.
    """
    monkeys = generate_monkey_list(input_str)

    max_worry = prod(x.divisor for x in monkeys)

    for _ in range(number_of_rounds):
        monkey_business(monkeys, worry_reduction, max_worry)

    total_items_inspected = [x.number_of_inspections for x in monkeys]
    total_items_inspected.sort(reverse=True)
    return total_items_inspected[0] * total_items_inspected[1]


def part_two(input_str: str) -> int:
    """
    Now  WORRY_REDUCTION == 1 and NUMBER_OF_ROUNDS = 10_000. Proceed as in part_one.

    We need to manage the worry levels somehow, since the actual number will now be massive.
    I'm sure cleverer ways exist but we can just subtract the product of all the divisors since
    we know that can't effect any of the modulo operations.
    """
    return part_one(input_str, number_of_rounds=10_000, worry_reduction=1)


test_input = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

assert part_one(test_input) == 10605
assert part_two(test_input) == 2713310158


if __name__ == "__main__":
    with open("input.txt") as flines:
        input_str = flines.read()

    print("part one:", part_one(input_str))
    print("part two:", part_two(input_str))
