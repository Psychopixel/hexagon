from enum import Enum
from math import pi

F_HEX = 0.866025404

# Define an Enum for directions
class Direction(Enum):
    RIGHT = 0
    DOWN_RIGHT = 1
    DOWN_LEFT = 2
    LEFT = 3
    UP_LEFT = 4
    UP_RIGHT = 5


# define the type of hex grid
class HexGridType:
    HORIZONTAL = pi / 2
    VERTICAL = 0.0

# define the contiguos hex
class Contiguos:
    HORIZONTAL_GRID_ODD_ROW_RANGE = [
            # even rows
            [[+1, 0], [+1, +1], [0, +1], [-1, 0], [0, -1], [+1, -1]],
            # odd rows
            [[+1, 0], [0, +1], [-1, +1], [-1, 0], [-1, -1], [0, -1]],
        ]

    HORIZONTAL_GRID_EVEN_ROW_RANGE = [
        # even rows
        [[+1, 0], [0, +1], [-1, +1], [-1, 0], [-1, -1], [0, -1]],
        # odd rows
        [[+1, 0], [+1, +1], [0, +1], [-1, 0], [0, -1], [+1, -1]],
    ]

    VERTICAL_GRID_ODD_COL_RANGE = [
        # even cols
        [[+1, 0], [0, +1], [-1, 0], [-1, -1], [0, -1], [+1, -1]],
        # odd cols
        [[+1, +1], [0, +1], [-1, +1], [-1, 0], [0, -1], [+1, 0]],
    ]

    VERTICAL_GRID_EVEN_COL_RANGE = [
        # even cols
        [[+1, 0], [0, +1], [-1, 0], [-1, -1], [0, -1], [+1, -1]],
        # odd cols
        [[+1, +1], [0, +1], [-1, +1], [-1, 0], [0, -1], [+1, 0]],
    ]
