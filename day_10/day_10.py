"""
day_10.py

Given a set of CPU instructions, find the values of its register <x> over time.

x starts with value 1.
There are two instructions:
addx <val> - takes two cycles to complete, then increases x by <val>
noop - takes one cycle, does nothing.


The X register controls a sprite position - the sprite is 3 pixels wide, and the X register
sets the horizontal position of the middle of the sprite.

This is tied to a CRT screen that is 40 rows wide and 6 high. The CRT draws a single pixel
each cycle - if one of the sprite's pixels is the one being drawn, then we illuminate. Otherwise,
we leave it.

"""


class CPU:
    SPRITE_WIDTH = 1  # 1 either side - total width 3
    SCREEN_WIDTH = 40

    def __init__(self) -> None:
        self.x = 1
        self.cycle_number = 0
        self.x_history = []  # the value of x at the start of each cycle.

    def addx(self, x: int):
        """Takes two cycles, increments x."""
        self.cycle_number += 2
        self.x_history.append(self.x)
        self.x_history.append(self.x)
        self.x += x

    def noop(self):
        """Takes one cycle, does nothing"""
        self.cycle_number += 1
        self.x_history.append(self.x)

    def signal_strength(self, cycle_number: int) -> int:
        """get the cycle number times the x value at that cycle number."""
        return cycle_number * self.x_history[cycle_number - 1]

    def parse_input(self, input_str: str):
        """Read the instruction set, find the x value over time."""
        for line in input_str.splitlines():
            instr, *args = line.split()
            if instr == "addx":
                self.addx(int(args[0]))
            elif instr == "noop":
                self.noop()
            else:
                raise ValueError("invalid instruction found.")

    def print_screen(self) -> str:
        """Use the x history to draw a 40-by-6 screen."""
        assert len(self.x_history) == 6 * 40
        screen = ""
        for pixel, sprite_position in enumerate(self.x_history):
            pixel_position = pixel % CPU.SCREEN_WIDTH
            if abs(sprite_position - pixel_position) <= CPU.SPRITE_WIDTH:
                screen += "#"
            else:
                screen += "."
            if pixel_position == CPU.SCREEN_WIDTH - 1:
                screen += "\n"
        return screen


def part_one(input_str: str) -> int:
    """
    Find the signal strength over time.
    The signal strength is x * the cycle number. We want the signal strength
    during the 20th cycle and every 40 cycles after that. Return the sum of
    those strengths.
    """
    cpu = CPU()
    cpu.parse_input(input_str)
    signal_strengths = []
    for cycle_number in range(20, len(cpu.x_history), 40):
        signal_strengths.append(cpu.signal_strength(cycle_number))
    return sum(signal_strengths)


def part_two(input_str: str) -> int:
    """Parse the instructions into a x-position and use this to draw an image.

    x is a 3-pixel-wide sprite, and one pixel is drawn per cycle.

    TODO: make this tick through time rather than parsing a history."""

    cpu = CPU()
    cpu.parse_input(input_str)
    screen_output = cpu.print_screen()
    return screen_output


with open("test_input.txt") as flines:
    test_input = flines.read()

assert part_one(test_input) == 13140

test_screen = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""

assert part_two(test_input) == test_screen

# assert part_two(test_input_two) == 36

if __name__ == "__main__":
    with open("input.txt") as flines:
        input_str = flines.read()

    print("part one:", part_one(input_str))
    print("part two:")
    print(part_two(input_str))
