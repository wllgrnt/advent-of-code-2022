"""
day_9.py

We have knot positions on a 2d grid, with heads H and tails T.
Given a series of moves of the head H, determine how the tail will
move.

The head and tail must always be touching (or overlapping - diagonal counts)

If the head is ever two steps directly away, the tail moves one step in that
direction. Otherwise, if they aren't touching and aren't in the same row or
column, the tail moves one step diagonally.
"""
from dataclasses import dataclass


def cast_to_magnitude(input_int: int) -> int:
    if input_int == 0:
        return 0
    elif input_int < 0:
        return -1
    else:
        return 1


class Knot:
    def __init__(self):
        self.i = 0
        self.j = 0
        self._positions = set([(0, 0)])

    def __iadd__(self, other: tuple):
        assert len(other) == 2
        self.i += other[0]
        self.j += other[1]
        return self

    def __str__(self) -> str:
        return f"({self.i}, {self.j})"

    def _is_touching(self, head: "Knot"):
        return abs(self.i - head.i) <= 1 and abs(self.j - head.j) <= 1

    def chase(self, head: "Knot"):
        if not self._is_touching(head):
            diff = [head.i - self.i, head.j - self.j]
            adjustment = [cast_to_magnitude(x) for x in diff]
            self.i += adjustment[0]
            self.j += adjustment[1]
            self._positions.add((self.i, self.j))

    @property
    def num_places_travelled(self):
        return len(self._positions)


@dataclass
class Translation:
    direction: tuple
    magnitude: int


def parse_input(input_str: str) -> list[Translation]:
    """convert a newline-separated string into a list of 2d translations."""
    translations = []
    for line in input_str.splitlines():
        direction, magnitude = line.split()
        magnitude = int(magnitude)
        match direction:
            case "R":
                translations.append(Translation((1, 0), magnitude))
            case "L":
                translations.append(Translation((-1, 0), magnitude))
            case "U":
                translations.append(Translation((0, 1), magnitude))
            case "D":
                translations.append(Translation((0, -1), magnitude))
            case _:
                raise ValueError("unknown direction encountered.")
    return translations


def part_one(input_str: str) -> int:
    """
    Simulate the movement of H and T around the grid. Return the number of
    places T visits.
    """
    translations = parse_input(input_str)
    head, tail = Knot(), Knot()
    for translation in translations:
        for _ in range(translation.magnitude):
            head += translation.direction
            tail.chase(head)

    answer = tail.num_places_travelled
    return answer


def part_two(input_str: str) -> int:
    """As above, but now there are ten knots, and each follows the one in front."""
    translations = parse_input(input_str)
    knots = [Knot() for _ in range(10)]
    head = knots[0]
    for translation in translations:
        for _ in range(translation.magnitude):
            head += translation.direction
            for i, tail in enumerate(knots[1:], start=1):
                tail.chase(knots[i - 1])
    answer = knots[-1].num_places_travelled
    return answer


test_input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

assert part_one(test_input) == 13

test_input_two = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
assert part_two(test_input_two) == 36

if __name__ == "__main__":
    with open("input.txt") as flines:
        input_str = flines.read()

    print("part one:", part_one(input_str))
    print("part two:", part_two(input_str))
