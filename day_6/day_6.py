"""
day_6.py

find the sequence of four characters that are all different in the datastream,
and return the position.

"""


def find_distinct_chars(input_str: str, number_of_chars: int) -> int:
    """
    Find the first string position where the previous `number_of_chars` chars
    are all different. No arg prepartion needed - the input is just a one-line string.
    """
    for i in range(number_of_chars, len(input_str)):
        chars = input_str[i - number_of_chars : i]
        if len(chars) == len(set(chars)):  # concise, but probably suboptimal perf
            return i
    else:
        raise ValueError("No four-char sequence found.")


def part_one(input_str: str) -> int:
    """
    Find the start-of-packet marker in an input string.

    This is the first string position where the previous four chars are all
    different.
    """
    return find_distinct_chars(input_str, number_of_chars=4)


def part_two(input_str: str) -> int:
    """
    Find the start-of-message marker in an input string.

    This is the first string position where the previous fourteen chars are all
    different.
    """
    return find_distinct_chars(input_str, number_of_chars=14)


test_inputs = [
    ["mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 19],
    ["bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23],
    ["nppdvjthqldpwncqszvftbrmjlhg", 6, 23],
    ["nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29],
    ["zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26],
]

for input, part_one_answer, part_two_answer in test_inputs:
    assert part_one(input) == part_one_answer
    assert part_two(input) == part_two_answer

if __name__ == "__main__":

    with open("input.txt") as flines:
        input_str = flines.read()

    print("part one:", part_one(input_str))
    print("part two:", part_two(input_str))
