from enum import Enum
from math import pi

# Define an Enum for directions
class Direction(Enum):
    RIGHT = 0
    DOWN_RIGHT = 1
    DOWN_LEFT = 2
    LEFT = 3
    UP_LEFT = 4
    UP_RIGHT = 5

# define the type of hex grid
class HexGridType():
    HORIZONTAL = pi/2
    VERTICAL = 0.