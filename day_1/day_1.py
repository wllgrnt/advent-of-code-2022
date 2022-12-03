"""day_1.py

Given a list of ints for each Elf, separate by blank lines,
get the max total.
"""


def parse_input(input_path: str) -> list[list[int]]:
    with open(input_path) as flines:
        input_data = []
        current_list = []
        for line in flines:
            if line.strip():
                current_list.append(int(line.strip()))
            else:
                input_data.append(current_list)
                current_list = []

    return input_data


if __name__ == "__main__":

    input_data = parse_input("input.txt")

    # part one - get the max
    max_cals = max(sum(x) for x in input_data)
    print("max:", max_cals)

    # part two - get the sum of the top three

    sorted_input = sorted(input_data, key=sum)

    top_three_cals = sum(sum(x) for x in sorted_input[-3:])
    print("top three sum:", top_three_cals)
