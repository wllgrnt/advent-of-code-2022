"""
day_8.py

Given a grid of ints representing tree heights, find the number of trees that
are visible from outside the grid when looking directly along a row or column.

Then find the max 'scenic score' accounting for the number of visible trees.
"""

import numpy as np


class Forest:
    """Holds trees, and visiblity checker method"""

    def __init__(self, input_str: str) -> None:
        self.tree_grid: np.ndarray = self._parse_input(input_str)

    def _parse_input(self, input_str: str) -> np.ndarray:
        grid = [list(map(int, line)) for line in input_str.splitlines()]
        return np.array(grid, dtype="i8")

    def __str__(self) -> str:
        return str(self.tree_grid)

    def tree_is_visible(self, i: int, j: int) -> bool:
        """Return True if along any direction the tree is taller than everything between
        itself and the grid edge."""
        tree_height = self.tree_grid[i, j]
        height, width = self.tree_grid.shape
        if i == 0 or i == height:
            return True
        if j == 0 or j == width:
            return True
        # north, east, south, west
        intervening_tree_directions = [
            self.tree_grid[:i, j],
            self.tree_grid[i, j + 1 :],
            self.tree_grid[i + 1 :, j],
            self.tree_grid[i, :j],
        ]

        for intervening_tree_line in intervening_tree_directions:
            if np.all(intervening_tree_line < tree_height):
                return True
        return False

    def tree_scenic_score(self, i: int, j: int) -> bool:
        """Return the multiple of the four viewing distances"""
        tree_height = self.tree_grid[i, j]
        height, width = self.tree_grid.shape
        if i == 0 or i == height:
            return 0  # if one distance is 0 the score is always 0
        if j == 0 or j == width:
            return 0  # if one distance is 0 the score is always 0

        # north, east, south, west (reverse north and west to account for viewing)
        intervening_tree_directions = [
            self.tree_grid[:i, j][::-1],
            self.tree_grid[i, j + 1 :],
            self.tree_grid[i + 1 :, j],
            self.tree_grid[i, :j][::-1],
        ]

        score = 1
        for intervening_tree_line in intervening_tree_directions:
            line_score = 0
            for tree in intervening_tree_line:
                line_score += 1
                if tree >= tree_height:
                    break
            score *= line_score
        return score

    def max_scenic_score(self) -> int:
        scores = []
        for (i, j), _ in np.ndenumerate(self.tree_grid):
            scores.append(self.tree_scenic_score(i, j))

        return max(scores)

    def number_of_visible_trees(self) -> int:
        num_visible = 0
        for (i, j), _ in np.ndenumerate(self.tree_grid):
            if self.tree_is_visible(i, j):
                num_visible += 1
        return num_visible


def part_one(input_str: str) -> int:
    """
    Find the trees in the tree that are visible - all trees between it and
    the grid edge are shorter than it.

    We will attempt to do this in a slightly dense fashion, by checking every
    tree in all four directions - better computational approaches likely exist.
    """

    forest = Forest(input_str)

    return forest.number_of_visible_trees()


def part_two(input_str: str) -> int:
    """
    Find the number of visible trees from each position on the grid, return the max score.

    Consider each direction, and count the number of trees before a higher or equal tree, + 1
    for that blocker tree. This is the viewing distance.
    The score is found by multiplying the four viewing distances.

    """
    forest = Forest(input_str)

    forest.tree_scenic_score(3, 2)

    return forest.max_scenic_score()


test_input = """30373
25512
65332
33549
35390
"""

assert part_one(test_input) == 21
assert part_two(test_input) == 8

if __name__ == "__main__":
    with open("input.txt") as flines:
        input_str = flines.read()

    print("part one:", part_one(input_str))
    print("part two:", part_two(input_str))
