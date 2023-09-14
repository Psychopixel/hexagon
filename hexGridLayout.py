import json

from kivy.uix.floatlayout import FloatLayout

from arrow import Arrow
from definition import *
from hexagon import Hexagon


class HexGridLayout(FloatLayout):
    def __init__(
        self, hex_size=100, xRange=1, yRange=1, versus=HexGridType.HORIZONTAL, **kwargs
    ):
        super().__init__(**kwargs)

        self.hex_size = hex_size
        self.hex_height = self.hex_size * 0.866
        self.xRange = xRange
        self.yRange = yRange
        self.versus = versus

        self.horizontalGridOddRowRange = [
            # even rows
            [[+1, 0], [+1, +1], [0, +1], [-1, 0], [0, -1], [+1, -1]],
            # odd rows
            [[+1, 0], [0, +1], [-1, +1], [-1, 0], [-1, -1], [0, -1]],
        ]

        self.horizontalGridEvenRowRange = [
            # even rows
            [[+1, 0], [0, +1], [-1, +1], [-1, 0], [-1, -1], [0, -1]],
            # odd rows
            [[+1, 0], [+1, +1], [0, +1], [-1, 0], [0, -1], [+1, -1]],
        ]

        self.verticalGridOddColRange = [
            # even cols
            [[+1, 0], [0, +1], [-1, 0], [-1, -1], [0, -1], [+1, -1]],
            # odd cols
            [[+1, +1], [0, +1], [-1, +1], [-1, 0], [0, -1], [+1, 0]],
        ]

        self.verticalGridEvenColRange = [
            # even cols
            [[+1, 0], [0, +1], [-1, 0], [-1, -1], [0, -1], [+1, -1]],
            # odd cols
            [[+1, +1], [0, +1], [-1, +1], [-1, 0], [0, -1], [+1, 0]],
        ]

        # Set size and position hints
        self.size_hint = (None, None)

        if self.versus == HexGridType.HORIZONTAL:
            self.size = (
                self.hex_height * (self.xRange * 2 + 1),
                self.hex_size * (self.yRange * 1.5)
                + (self.hex_height - (self.hex_height * 0.866 / 2)),
            )
        else:
            self.size = (
                self.hex_size * self.xRange
                + self.hex_size * 0.866 * (self.xRange / 2 + self.xRange % 2),
                self.hex_size * 0.866 * 2 * self.yRange + self.hex_size * 0.866 / 2,
            )

        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.arrow = Arrow(self.versus)


    def load_hex_data(self, filename="hex_data.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            return data
        except Exception as e:
            print(f"Error loading hex data: {e}")
            return {}

    def create_hex(self, center_x, center_y, hex_data, *args):
        hex_data = self.load_hex_data()
        for x in range(self.xRange):
            for y in range(self.yRange):
                hex_id = f"hex_{x}_{self.yRange - y -1}"
                hex_attrs = hex_data.get(hex_id, {})
                hexagon = Hexagon(
                    self.hex_size,
                    0,
                    0,
                    125,
                    1,
                    0,
                    0,
                    1,
                    1,
                    2,
                    x,
                    y,
                    self.xRange,
                    self.yRange,
                    self.versus,
                    terrain=hex_attrs.get("terrain", ""),
                    color=hex_attrs.get("color", None),
                    content=hex_attrs.get("content", ""),
                )
                if self.versus == HexGridType.HORIZONTAL:
                    hexagon.pos = (
                        x * (self.hex_height * 2)
                        + ((y + 1) % 2 * self.hex_height)
                        + center_x
                        - self.width / 2
                        - (self.hex_size - self.hex_height),
                        (y * self.hex_size * 1.5) + center_y - self.height / 2,
                    )
                else:
                    hexagon.pos = (
                        x * (self.hex_size * 1.5) + center_x - self.width / 2,
                        y * (self.hex_height * 2)
                        + ((x + 1) % 2 * self.hex_height)
                        + center_y
                        - self.height / 2
                        - (self.hex_size - self.hex_height),
                    )
                new_id = f"hex_{x}_{self.yRange - y -1}"
                self.ids[new_id] = hexagon
                self.add_widget(hexagon)
        pass

    def create_arrow(self):
        self.add_widget(self.arrow)
        pass

    def setArrow(self, hex, direction):
        self.arrow.moveArrow(
            self.getHexCenter(hex), self.ids[hex].xCoord, self.ids[hex].yCoord
        )
        self.arrow.rotateButton(direction)

    def moveArrow(self, hex):
        self.arrow.moveArrow(
            self.getHexCenter(hex), self.ids[hex].xCoord, self.ids[hex].yCoord
        )

    def rotateArrow(self, new_direction):
        self.arrow.rotateButton(new_direction)

    def getArrow(self):
        return self.arrow.xCoord, self.arrow.yCoord, self.arrow.direction

    def getHexCenter(self, hex_name):
        return (
            self.ids[hex_name].center_x + self.arrow.arrow_button.width / 2,
            self.ids[hex_name].center_y + self.arrow.arrow_button.height / 2,
        )

    def getAllContiguos(self, yRange, xRange, arrow_y, arrow_x, gridVersus):
        neibourghs = []
        parity_row = arrow_y & 1
        parity_col = arrow_x & 1
        even = 0
        odd = 1
        if gridVersus == HexGridType.HORIZONTAL:
            # odd_r or even_r
            if yRange % 2 == 0:
                # even_r
                if parity_row == 0:
                    # even row
                    neibourghs = self.horizontalGridEvenRowRange[even].copy()
                else:
                    # odd row
                    neibourghs = self.horizontalGridEvenRowRange[odd].copy()
            else:
                # odd_r
                if parity_row == 0:
                    # even row
                    neibourghs = self.horizontalGridOddRowRange[even].copy()
                else:
                    # odd row
                    neibourghs = self.horizontalGridOddRowRange[odd].copy()
        else:
            # odd_q or even_q
            if xRange % 2 == 0:
                # even_q
                if parity_col == 0:
                    # even col
                    neibourghs = self.verticalGridEvenColRange[even].copy()
                else:
                    # odd col
                    neibourghs = self.verticalGridEvenColRange[odd].copy()
            else:
                # odd_q
                if parity_col == 0:
                    # even col
                    neibourghs = self.verticalGridOddColRange[even].copy()
                else:
                    # odd col
                    neibourghs = self.verticalGridOddColRange[odd].copy()
        return neibourghs

    def getPossibleHex(self, contiguos, direction):
        if direction == 0:
            clickable = [contiguos[5], contiguos[0], contiguos[1]]
        elif direction == 1:
            clickable = [contiguos[0], contiguos[1], contiguos[2]]
        elif direction == 2:
            clickable = [contiguos[1], contiguos[2], contiguos[3]]
        elif direction == 3:
            clickable = [contiguos[2], contiguos[3], contiguos[4]]
        elif direction == 4:
            clickable = [contiguos[3], contiguos[4], contiguos[5]]
        else:
            clickable = [contiguos[4], contiguos[5], contiguos[0]]
        return clickable

    def getMove(self, possibleHex, hexClicked, arrow_x, arrow_y, direction):
        cnt = 0
        for possible in possibleHex:
            newHex = [possible[0] + arrow_x, possible[1] + arrow_y]
            if newHex == hexClicked:
                if cnt == 0:
                    newDirection = direction - 1
                    if newDirection < 0:
                        newDirection = 5
                    return f"rotate_{newDirection}"
                elif cnt == 1:
                    return "move"
                else:
                    newDirection = direction + 1
                    if newDirection > 5:
                        newDirection = 0
                    return f"rotate_{newDirection}"
            cnt += 1
        return None

    def calculateMove(self, instance):
        arrow_x, arrow_y, arrow_direction = self.getArrow()
        move = self.getMove(
            self.getPossibleHex(
                self.getAllContiguos(
                    yRange=self.yRange,
                    xRange=self.xRange,
                    arrow_x=arrow_x,
                    arrow_y=arrow_y,
                    gridVersus=self.versus,
                ),
                direction=arrow_direction,
            ),
            [instance.xCoord, instance.yCoord],
            arrow_x=arrow_x,
            arrow_y=arrow_y,
            direction=arrow_direction,
        )
        return move

    def do_layout(self, *args):
        pass
