"""
day_12.py - hill climbing

Inputs: a 2d grid of chars where a marks the lowest elevation and z the highest,
and your current position S (height a) and desired location E (height z), find out
how to get from S to E in as few steps as possible.

You can only move to a square <= 1 higher than the current one.
"""
import networkx as nx
import numpy as np
import string


def parse_input(input_str: str) -> tuple[np.array, tuple[int], tuple[int]]:
    """Return the grid as a 2d numpy integer array, and the start and end coordinates"""
    grid = np.array([list(x) for x in input_str.splitlines()])
    start_coords = tuple(np.argwhere(grid == "S")[0])
    end_coords = tuple(np.argwhere(grid == "E")[0])

    grid[tuple(start_coords)] = "a"
    grid[tuple(end_coords)] = "z"

    char_to_number = lambda x: string.ascii_lowercase.index(x)

    return np.vectorize(char_to_number)(grid), start_coords, end_coords


def get_neighbour_indices(grid, position):
    max_i, max_j = grid.shape
    indices = []
    i, j = position
    if i > 0:
        indices.append((i - 1, j))
    if i < max_i - 1:
        indices.append((i + 1, j))
    if j > 0:
        indices.append((i, j - 1))
    if j < max_j - 1:
        indices.append((i, j + 1))
    return indices


# BELOW - A RECURSIVE VERSION THAT I BELIEVE WORKS, BUT HITS PYTHON RECURSION LIMITS (IE DOESN'T WORK)
# def find_min_steps(grid, traversed, start_coords, end_coords, current_steps=-1):
#     """Look at all un-looked-at neighbours of start-coords. Find the shortest path from each to end-coords.

#     Then choose the min, updating traversed to avoid cycles.
#     """
#     neighbours = get_neighbour_indices(grid, start_coords)
#     reachable_neighbours = []
#     for neighbour in neighbours:
#         if traversed[neighbour]:
#             continue
#         else:
#             if (grid[neighbour] - grid[start_coords]) <= 1:
#                 # then its reachable - either you've found the end coods, or you must continue the search.
#                 if neighbour == end_coords:
#                     return current_steps
#                 reachable_neighbours.append(neighbour)
#                 traversed[neighbour] = True
#     if not reachable_neighbours:
#         # you are in a corner - bail out, penalise this branch.
#         return 100000000000000000000
#     print('  '*current_steps, reachable_neighbours)
#     return min(find_min_steps(grid, traversed, x, end_coords, current_steps=current_steps+1) for x in reachable_neighbours)


def build_graph(grid):
    """Build an directed graph of all reachable routes."""
    graph = nx.DiGraph()
    for index in np.ndindex(grid.shape):
        for neighbour in get_neighbour_indices(grid, index):
            if grid[neighbour] - grid[index] <= 1:
                graph.add_edge(u_of_edge=tuple(index), v_of_edge=tuple(neighbour))
    return graph


def part_one(input_str: str) -> int:
    """
    Find the shortest path between S and E on a 2D grid.

    Following a failed recursive effort (above), this cheats by building a graph and then
    handing off the hard work to networkx's inbuilt Dijkstra's implementation.
    """
    grid, start_coords, end_coords = parse_input(input_str)
    grid_graph = build_graph(grid)

    return nx.shortest_path_length(G=grid_graph, source=start_coords, target=end_coords)


def part_two(input_str: str) -> int:
    """
    Find the shortest path from any path at elevation a to E.
    """
    grid, start_coords, end_coords = parse_input(input_str)
    grid_graph = build_graph(grid)
    start_points = [tuple(x) for x in np.argwhere(grid == 0)]

    shortest_paths = []
    for x in start_points:
        try:
            shortest_paths.append(
                nx.shortest_path_length(G=grid_graph, source=x, target=end_coords)
            )
        except nx.NetworkXNoPath:
            continue
    return min(shortest_paths)


test_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

assert part_one(test_input) == 31
assert part_two(test_input) == 29


if __name__ == "__main__":
    with open("input.txt") as flines:
        input_str = flines.read()

    print("part one:", part_one(input_str))
    print("part two:", part_two(input_str))
