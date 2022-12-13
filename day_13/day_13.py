"""
day_13.py - distress signal

You receive pairs of packets, and must identify which packets are in the right order.
Packet data is lists and integers - we have comparison rules determining how they
should be ordered.
"""
from dataclasses import dataclass
from itertools import zip_longest


@dataclass
class Packet:
    """Used in part two as a convenience wrapper for sorted()"""

    raw_packet: list

    def __lt__(self, other: "Packet") -> bool:
        return compare(self.raw_packet, other.raw_packet)


def parse_input(input_str: str) -> list[tuple[list, list]]:
    """Generate a list of left/right pairs of nested lists."""
    packets = []
    for packet in input_str.split("\n\n"):
        left, right = (eval(x) for x in packet.splitlines())
        packets.append((left, right))
    return packets


def compare(left: list, right: list) -> bool | None:
    """Recursively compare nested lists.

    Rules:
    - If both values are integers, the lower integer comes first, or they are equal.
    - If both values are lists, compare the first value, the second, etc.
        The left list should run out of items first, or be equal.
    - If one value is an integer, convert the integer to a single-member list and try
        again.
    """
    if type(left) is int and type(right) is int:
        # do int comparison
        if left == right:
            return None
        else:
            return left < right
    elif type(left) is list and type(right) is list:
        # do list comparison - compare the values in order.
        for x, y in zip_longest(left, right, fillvalue=None):
            if y is None:
                return False
            elif x is None:
                return True
            else:
                result = compare(x, y)
                if result is not None:
                    return result

    else:
        # convert both to list, try again
        if type(left) is int:
            return compare([left], right)
        else:
            return compare(left, [right])


def part_one(input_str: str) -> int:
    """
    Split the `input_str` into pairs of packets - left and right.
    Compare using given rules to check if they are correctly ordered.
    Return the sum of the indices of correctly-order packets.
    """
    packets = parse_input(input_str)
    correct_packet_indices = []
    for i, packet in enumerate(packets):
        left, right = packet
        if compare(left, right):
            correct_packet_indices.append(i + 1)  # problem uses 1-based indexing
    return sum(correct_packet_indices)


def part_two(input_str: str) -> int:
    """
    Use the comparison rules from part one to order all the packets plus two dividers.
    Then return the indicies of the two dividers, multiplied together.
    """
    packets = parse_input(input_str)
    dividers = ([[2]], [[6]])
    packets.append(dividers)
    # flatten
    packets_flattened = [Packet(packet) for pair in packets for packet in pair]
    # sort, given true/false comparisons. Easiest to override < operator and use sorted()
    sorted_packets = sorted(packets_flattened)

    decoder_key = 1
    for i, packet in enumerate(sorted_packets):
        if packet.raw_packet in dividers:
            decoder_key *= i + 1

    return decoder_key


test_input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

assert part_one(test_input) == 13
assert part_two(test_input) == 140


if __name__ == "__main__":
    with open("input.txt") as flines:
        input_str = flines.read()

    print("part one:", part_one(input_str))
    print("part two:", part_two(input_str))
