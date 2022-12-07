"""
day_7.py

given some terminal history, and a filesystem consisting
of files + dirs, with root /, we have commands:

cd (.., /, x), where x is a dir in the current directory
ls

Build the filesystem and determine the total size of each directory.
"""

"""
idea: a Directory class, which has a size() property, and a contents attribute.
Contents is a list, of either Files or Directories. Files have size an int, Dirs have size
the sizes of their contents.

Then run some tree traversal to grab the big dirs.
"""
TOTAL_DISK_SIZE = 70_000_000
FREE_SPACE_REQUIRED = 30_000_000
LARGE_DIR_SIZE = 100_000


FileObject = list["Directory", "File"]


class Directory:
    """Holds a list of other dirs and files, and a size property that is the
    sum of their childrens' sizes.
    """

    def __init__(self, name: str, parent_dir=None) -> None:
        self.name = name
        self.contents: dict[str, FileObject] = {}  # map from dir name to FileObject
        self.parent_dir = parent_dir  # a Directory, unless you are the root dir.
        self.root_dir = None

    @property
    def size(self) -> int:
        return sum(x.size for x in self.contents.values())

    def __str__(self) -> str:
        return f"Directory {self.name} with contents: {list(self.contents.keys())}"


class File:
    """Just has a name and a size. Properties overkill here."""

    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size


class Terminal:
    def __init__(self, history: str) -> None:
        self.current_dir: Directory | None = None
        self.history = history

    def replay_history(self) -> Directory:
        """Replay the terminal history to generate a directory structure.

        Inputs are a set of commands, marked by $. Parse the commands to track
        what dir you're in, and parse the output to populate the dirs.

        Returns:
            The final directory you inhabit.
        """
        for term_section in self.history.split("$")[
            1:
        ]:  # drop the first (empty) command.
            commands = term_section.split("\n")
            command = commands[0].strip()
            output = [x for x in commands[1:] if x]
            self._parse_command(command, output)
        return self.current_dir

    def _parse_command(self, command: str, output: list[str]):
        """use the commands to change and populate the filesystem.

        two options: cd <dir>, or ls.
        """
        command, *args = command.split(" ")
        if command == "ls":
            assert not args
            self._ls(output)

        elif command == "cd":
            assert not any(output)
            dir = args[0]
            self._cd(dir)
        else:
            raise ValueError("unknown command encountered", command)

    def _cd(self, directory: str):
        """Options are /, .., or a directory in the current dir."""
        if directory == "/":
            # NB: we can only currently run this once, and it must be first
            assert self.current_dir is None
            self.current_dir = Directory("/", parent_dir=None)
            self.root_dir = self.current_dir
        elif directory == "..":
            self.current_dir = self.current_dir.parent_dir
        else:
            self.current_dir = self.current_dir.contents[directory]

    def _ls(self, file_contents: list[str]):
        """Use the output of ls to populate the current dirs contents.

        Args:
            file_contents: should be a list of space-separated pairs.
        """
        for file_content in file_contents:
            file_size, file_name = file_content.split()
            if file_size == "dir":
                self.current_dir.contents[file_name] = Directory(
                    file_name, parent_dir=self.current_dir
                )
            else:
                self.current_dir.contents[file_name] = File(
                    name=file_name, size=int(file_size)
                )


def part_one(input_str: str) -> int:
    """Parse the input string into a directory structure, then traverse to
    find the directories smaller than `LARGE_DIR_SIZE`.
    """
    terminal = Terminal(input_str)
    _ = terminal.replay_history()
    root = terminal.root_dir
    # walk through the directories, looking for ones exceeding the size given.
    small_dirs = []

    def _traverse(dir):
        for dir in dir.contents.values():
            if isinstance(dir, Directory):
                if dir.size < LARGE_DIR_SIZE:
                    small_dirs.append([dir.name, dir.size])
                _traverse(dir)

    _traverse(root)
    return sum(x[1] for x in small_dirs)


def part_two(input_str: str) -> int:
    """Parse the input string into a directory structure, then traverse to
    find the smallest directory freeing up the space."""

    terminal = Terminal(input_str)
    _ = terminal.replay_history()
    root = terminal.root_dir
    # walk through the directories, pull all sizes
    dir_sizes = []

    def _traverse(dir):
        for dir in dir.contents.values():
            if isinstance(dir, Directory):
                dir_sizes.append([dir.name, dir.size])
                _traverse(dir)

    _traverse(root)

    current_space = TOTAL_DISK_SIZE - root.size
    space_to_free = FREE_SPACE_REQUIRED - current_space
    minimum_viable_size = sorted([y for x, y in dir_sizes if y >= space_to_free])[0]

    return minimum_viable_size


test_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

assert part_one(test_input) == 95437
assert part_two(test_input) == 24933642

if __name__ == "__main__":
    with open("input.txt") as flines:
        input_str = flines.read()

    print("part one:", part_one(input_str))
    print("part two:", part_two(input_str))
