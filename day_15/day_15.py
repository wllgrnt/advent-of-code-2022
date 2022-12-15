"""
day_15.py - Beacon Exclusion Zone

You have a set of beacons and sensors - each sensor detects the closet beacon
by Manhattan distance. So you have exclusion zones where the distress beacon
cannot be.
Part one - find the exclusion zone for a given row.

"""
import re
from tqdm import tqdm


def parse_input(input_str) -> list[tuple[(int, int), (int, int), int]]:

    output = []
    for line in input_str.splitlines():
        sensor_x, sensor_y, beacon_x, beacon_y = [
            int(x) for x in re.findall(r"-?\d+", line)
        ]
        distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        output.append(((sensor_x, sensor_y), (beacon_x, beacon_y), distance))
    return output


def part_one(input_str: str, row_number: int) -> int:
    """
    Given a set of sensors and beacons, find the exclusion zone for each beacon
    and thus the places where the distress beacon cannot be for y=`row_number`.

    Need to find the overlap of the exclusion zone with row_number, which we do by finding all the
    beacons within the distance of our row
    """

    sensors_and_distances = parse_input(input_str)

    excluded_x_positions = set()  # do set stuff to track overlaps.
    beacons_on_row = set()
    for sensor, beacon, distance in sensors_and_distances:
        y_distance = abs(sensor[1] - row_number)
        if beacon[1] == row_number:
            beacons_on_row.add(beacon)
        if y_distance <= distance:
            lower_exclusion = sensor[0] - abs(
                y_distance - distance
            )  # the lower x position that is excluded.
            upper_exclusion = sensor[0] + abs(
                y_distance - distance
            )  # the upper x position that is excluded.
            new_x_positions = list(range(lower_exclusion, upper_exclusion + 1))
            excluded_x_positions.update(new_x_positions)

    # i think we have to exclude spaces with beacons from our coverage region? doesn't make much sense.
    return len(excluded_x_positions) - len(beacons_on_row)


# # The below requires a terabyte of ram for the problem size. And brute-forcing by iterating over coords would
# # take 1000 hours
# def part_two(input_str: str, space_size: int) -> int:
#     """Rather than viewing a single row, use the whole space, given the space size."""

#     space = np.ones(shape=(space_size, space_size), dtype=bool)
#     indices = np.argwhere(space)

#     sensors_and_distances = parse_input(input_str)

#     for sensor, beacon, distance in sensors_and_distances:
#         # Find the indices of all points in the array
#         # Calculate the Manhattan distance of each point from the given point
#         manhattan_distances = np.abs(indices - sensor)
#         manhattan_distances = np.sum(manhattan_distances, axis=1).reshape(
#             (space_size, space_size)
#         )

#         # Select only the points that are within the desired distance
#         space[manhattan_distances <= distance] = False
#     assert len(np.argwhere(space)) == 1

#     beacon_x, beacon_y = np.argwhere(space)[0]
#     return beacon_x * 4000000 + beacon_y


def get_diamond(centre_point: tuple, distance: int, space_size):
    """generate the set of points `distance` away from the centre"""
    # this is dumb but easy
    centre_x, centre_y = centre_point

    points = []
    x = centre_x + distance
    y = centre_y
    for i in range(distance + 1):
        points.append((x - i, y + i))
    x, y = points[-1]
    for i in range(1, distance + 1):
        points.append((x - i, y - i))
    x, y = points[-1]
    for i in range(1, distance + 1):
        points.append((x + i, y - i))
    x, y = points[-1]
    for i in range(1, distance + 1):
        points.append((x + i, y + i))

    return [(x, y) for x, y in points if 0 <= x <= space_size and 0 <= y <= space_size]


def part_two(input_str: str, space_size: int) -> int:
    """Find the one place in the space not excluded.

    Copying from existing answers, we use the fact that our search space
    is going to be in a ring 1 unit further than the beacon for each sensor.

    Generate that space, and iterate.
    """

    sensors_and_distances: list[tuple[(int, int), (int, int), int]] = parse_input(
        input_str
    )

    # generate the search space.
    possible_beacon_points = []
    for sensor, beacon, distance in sensors_and_distances:
        possible_beacon_points += get_diamond(
            sensor, distance=distance + 1, space_size=space_size
        )

    for point in tqdm(possible_beacon_points):
        for sensor, beacon, distance in sensors_and_distances:
            if abs(sensor[0] - point[0]) + abs(sensor[1] - point[1]) <= distance:
                break
        else:
            return point[0] * 4_000_000 + point[1]


test_input = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

assert part_one(test_input, 10) == 26
assert part_two(test_input, 20) == 56000011


if __name__ == "__main__":
    with open("input.txt") as flines:
        input_str = flines.read()

    print("part one:", part_one(input_str, 2_000_000))
    print("part two:", part_two(input_str, 4_000_000))
