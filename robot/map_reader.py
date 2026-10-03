"""Map reader for the Autonomous Robot Navigation project.

Students complete TWO tasks:

1. read_txt_map()
   Read the txt file and convert it to a nested list of symbols.

2. convert_to_cost_map()
   Convert the symbol map to a nested list of costs.

Teacher code:
    validate_raw_map()
    validate_cost_map()
    get_map_info()

Map symbols:
    . = normal cell
    S = start
    G = goal
    B = bonus
    # = obstacle

For Challenge 4:
    g = grass
    M = mud
    W = water

The assignment uses G for both Goal and Grass.
This starter project uses lowercase g for Grass.

Coordinates are (row, column).
The top-left cell is (0, 0).
"""


def read_txt_map(filename):
    """Read a txt map and return a nested list of symbols.

    Example txt file:

        ..G
        .#.
        S..

    Expected return value:

        [
            ['.', '.', 'G'],
            ['.', '#', '.'],
            ['S', '.', '.']
        ]
    """

    raw_map = []

    # ============================================================
    # STUDENT TASK 1
    # ============================================================
    # 1. Open filename using UTF-8.
    # 2. Read the file line by line.
    # 3. Remove the line ending.
    # 4. Skip blank lines.
    # 5. Convert each row to a list of characters.
    # 6. Append each row to raw_map.
    #
    # IMPORTANT:
    # '#' means obstacle. It is NOT a comment in the txt file.
    with open(filename,"r",encoding="utf-8")as f:
        for line in f:
            line =line.rstrip("\n")
            if not line :
                continue
            row_chars =list(line)
            raw_map.append(row_chars)
    return raw_map


def convert_to_cost_map(raw_map):
    """Convert a symbol map into a cost map.

    Rules:

        . = 1
        S = 1
        G = 1
        B = 1
        # = None

    Challenge 4 terrain:

        g = 2
        M = 5
        W = 10

    Example:

        [
            ['.', '#'],
            ['S', 'G']
        ]

    becomes:

        [
            [1, None],
            [1, 1]
        ]
    """

    cost_map = []

    # ============================================================
    # STUDENT TASK 2
    # ============================================================
    # Convert every symbol in raw_map into its corresponding cost.
    # The shape of cost_map must be the same as raw_map.
    cost_lookup={
        ".":1,
        "S":1,
        "G":1,
        "B":1,
        "#":None,
        "g":2,
        "M":5,
        "W":10
    }
    for row in raw_map:
        cost_row=[]
        for symbol in row :
            cost_row.append(cost_lookup[symbol])
        cost_map.append(cost_row)
    return cost_map


# ================================================================
# TEACHER CODE BELOW
# Students do not need to modify these functions.
# ================================================================

def validate_raw_map(raw_map):
    """Check whether the symbol map follows the project rules."""

    if not isinstance(raw_map, list) or len(raw_map) == 0:
        raise ValueError("raw_map must be a non-empty list")

    if not isinstance(raw_map[0], list) or len(raw_map[0]) == 0:
        raise ValueError("Each row of raw_map must be a non-empty list")

    width = len(raw_map[0])
    valid_symbols = ".SGB#gMW"

    start_count = 0
    goal_count = 0

    for row in raw_map:
        if not isinstance(row, list):
            raise ValueError("Each row of raw_map must be a list")

        if len(row) != width:
            raise ValueError("All rows must have the same length")

        for cell in row:
            if cell not in valid_symbols:
                raise ValueError("Unknown map symbol: " + str(cell))

            if cell == "S":
                start_count += 1

            if cell == "G":
                goal_count += 1

    if start_count != 1:
        raise ValueError("Map must contain exactly one S")

    if goal_count != 1:
        raise ValueError("Map must contain exactly one G")

    return True


def validate_cost_map(raw_map, cost_map):
    """Check whether the student's cost_map is correct."""

    if not isinstance(cost_map, list):
        raise ValueError("cost_map must be a list")

    if len(cost_map) != len(raw_map):
        raise ValueError("cost_map has the wrong number of rows")

    expected_cost = {
        ".": 1,
        "S": 1,
        "G": 1,
        "B": 1,
        "#": None,
        "g": 2,
        "M": 5,
        "W": 10,
    }

    for row in range(len(raw_map)):
        if not isinstance(cost_map[row], list):
            raise ValueError("Each row of cost_map must be a list")

        if len(cost_map[row]) != len(raw_map[row]):
            raise ValueError("cost_map has the wrong number of columns")

        for col in range(len(raw_map[row])):
            symbol = raw_map[row][col]
            expected = expected_cost[symbol]
            actual = cost_map[row][col]

            if actual != expected:
                raise ValueError(
                    "Wrong cost at "
                    + str((row, col))
                    + ": expected "
                    + str(expected)
                    + ", got "
                    + str(actual)
                )

    return True


def get_map_info(raw_map):
    """Return start, goal, and bonus positions from the symbol map."""

    start = None
    goal = None
    bonuses = []

    for row in range(len(raw_map)):
        for col in range(len(raw_map[row])):
            cell = raw_map[row][col]

            if cell == "S":
                start = (row, col)

            elif cell == "G":
                goal = (row, col)

            elif cell == "B":
                bonuses.append((row, col))

    return start, goal, bonuses
