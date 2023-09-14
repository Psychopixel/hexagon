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
                self.hex_size * (self.yRange * 1.5)
                + (self.hex_height - (self.hex_height * 0.866 / 2)),
                self.hex_height * (self.xRange * 2 + 1),
            )
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.arrow = Arrow(self.versus)

    def create_hex(self, center_x, center_y, *args):
        for x in range(self.xRange):
            for y in range(self.yRange):
                hexagon = Hexagon(
                    self.hex_size,
                    x % 2,
                    0,
                    y % 2,
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

    def do_layout(self, *args):
        pass
