"""
day_14.py - regolith reservoir

We are given path co-ordinates representing rock profiles, and the
knowledge that sand is pouring in at co-ordinate (500,0)

sand is produced one unit at a time, once the previous unit has come
to rest. Sand falls downwards if possible, if not, if falls down and left.
if not either of those, then down and right.

part one - how much sand falls before the system stabilises?
"""
import numpy as np

Point = tuple[int, int]
SAND_COORDS = (500, 0)


def parse_input(input_str: str) -> np.ndarray:
    # this is double-counting the intermediate points, but that's fine.
    coords = []
    for line in input_str.splitlines():
        prev_coord = None
        for coord in line.split(" -> "):
            x, y = coord.split(",")
            new_coord = (int(x), int(y))
            if prev_coord is not None:
                line_coords = interpolate(prev_coord, new_coord)
                coords += line_coords
            prev_coord = new_coord
    return coords


def generate_matrix_from_coords(coord_list: list[Point]) -> tuple[np.ndarray, Point]:
    """ascertain the limits of the coord list and return a boolean array,
    plus the point that sand is generated from."""
    xs = [SAND_COORDS[0]] + [coord[0] for coord in coord_list]
    ys = [SAND_COORDS[1]] + [coord[1] for coord in coord_list]
    min_x, max_x, min_y, max_y = (min(xs), max(xs), min(ys), max(ys))
    matrix = np.zeros((max_x - min_x + 1, max_y - min_y + 1), dtype=bool)
    for x, y in coord_list:
        matrix[x - min_x, y - min_y] = True

    return matrix, (SAND_COORDS[0] - min_x, SAND_COORDS[1] - min_y)


def interpolate(start_point: Point, end_point: Point) -> list[Point]:
    """returns all the points between `start_point` and `end_point` inclusive."""
    start_x, start_y = start_point
    end_x, end_y = end_point
    coords = []
    if start_x == end_x:
        # take smaller point as first wlog.
        start = min(start_y, end_y)
        stop = max(start_y, end_y)
        for y in range(start, stop + 1):
            coords.append((start_x, y))
    elif start_y == end_y:
        start = min(start_x, end_x)
        stop = max(start_x, end_x)
        for x in range(start, stop + 1):
            coords.append((x, start_y))
    else:
        raise ValueError("lines must be horizontal or vertical.")
    return coords


class CaveProfile:
    def __init__(self, input_str: str) -> None:
        self.rock_coords = parse_input(input_str)
        self.rock_matrix, self.sand_point = generate_matrix_from_coords(
            self.rock_coords
        )

    def __str__(self) -> str:
        output_str = ""
        for row in self.rock_matrix.T:
            for val in row:
                if val:
                    output_str += "#"
                else:
                    output_str += "."
            output_str += "\n"
        return output_str

    def next_move(self, coord) -> None | Point:
        """try, in order, straight down, down and left, down and right.

        if nothing's going return None
        """
        x, y = coord
        for pair in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]:
            try:
                next_coord = self.rock_matrix[pair]
                if not next_coord:
                    return pair
            except IndexError:
                return (-1, -1)

        return None

    def propagate_sand(self) -> int:
        """Create a sand point at self.sand_point.
        Move it down until it has no moves or falls off the limits, then add
        it to rock_matrix and increment a counter. Return the final count when
        the matrix is stable.
        """
        counter = 0
        max_possible_moves = self.rock_matrix.shape[1]
        prev_state = self.rock_matrix.sum()
        while True:
            current_position = self.sand_point
            next_position = current_position
            for _ in range(max_possible_moves):
                next_position = self.next_move(current_position)
                if next_position is None:
                    self.rock_matrix[current_position] = True
                    counter += 1
                    break
                current_position = next_position

            if self.rock_matrix.sum() == prev_state:
                return counter
            prev_state = self.rock_matrix.sum()

    def add_floor(self):
        """Add a floor two blocks below the bottom filled block."""
        current_width, current_height = self.rock_matrix.shape
        new_rock_matrix = np.zeros(
            shape=(current_width + (current_height * 2), current_height + 2), dtype=bool
        )
        new_rock_matrix[
            current_height : current_width + current_height, :current_height
        ] = self.rock_matrix
        new_rock_matrix[:, -1] = True
        self.rock_matrix = new_rock_matrix
        self.sand_point = (self.sand_point[0] + current_height, self.sand_point[1])


def part_one(input_str: str) -> int:
    """Allow sand to fall, return the total grains emitted."""
    cave = CaveProfile(input_str)
    counter = cave.propagate_sand()
    return counter


def part_two(input_str: str) -> int:
    """As in part one, but now introduce a floor:
    - extend the matrix by its height in either direction, plus add 2 to the bottom, and fill this in.
    """
    cave = CaveProfile(input_str)
    # -1 to account for the new end condition, which is when a block covers the sand emission point
    cave.add_floor()
    counter = cave.propagate_sand()
    return counter - 1


test_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

assert part_one(test_input) == 24
assert part_two(test_input) == 93


if __name__ == "__main__":
    with open("input.txt") as flines:
        input_str = flines.read()

    print("part one:", part_one(input_str))
    print("part two:", part_two(input_str))
