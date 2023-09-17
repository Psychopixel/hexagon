import json

from kivy.uix.floatlayout import FloatLayout

from arrow import Arrow
from definition import *
from hexagon import Hexagon

class HexGridLayout(FloatLayout):
    def __init__(
        self, hex_radius=100, xRange=1, yRange=1, versus=HexGridType.HORIZONTAL, **kwargs
    ):
        super().__init__(**kwargs)

        self.hex_radius = hex_radius
        self.hex_innerRadius = self.hex_radius * F_HEX
        self.xRange = xRange
        self.yRange = yRange
        self.versus = versus

        # Set size and position hints
        self.size_hint = (None, None)

        if self.versus == HexGridType.HORIZONTAL:
            self.size = (
                self.hex_innerRadius * (self.xRange * 2 + 1),
                self.hex_radius * (self.yRange * 1.5)
                + (self.hex_innerRadius - (self.hex_innerRadius * F_HEX / 2)),
            )
        else:
            self.size = (
                self.hex_radius * self.xRange
                + self.hex_radius * F_HEX * (self.xRange / 2 + self.xRange % 2),
                self.hex_radius * F_HEX * 2 * self.yRange + self.hex_radius * F_HEX / 2,
            )

        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.arrow = Arrow(self.versus)
        fileName = AppPath.resource_path("map_data.json")
        mapData = self.load_map_data(fileName)
        self.default_hex = mapData.get("default_hex")
        self.hex_type = mapData.get("type")
        self.grid = mapData.get("grid")

    def getType(self, id):
        for hexType in self.hex_type:
            if hexType["id"] == id:
                return hexType
        print(f"Errore, id {id} non trovato!")
        return None

    def load_map_data(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            return data
        except Exception as e:
            print(f"Error loading map data: {e}")
            return {}

    def create_hex(self, center_x, center_y, *args):
        bg_r, bg_g, bg_b, bg_a = self.default_hex.get("background_color", [0, 0, 125, 1])
        stroke_r, stroke_g, stroke_b, stroke_a = self.default_hex.get("stroke_color", [0, 0, 0, 1])
        stroke_thickness = self.default_hex.get("stroke_thickness", 2)
        for x in range(self.xRange):
            for y in range(self.yRange):
                yy = self.yRange - y -1
                #hex_id = f"hex_{x}_{self.yRange - y -1}"
                hex_attrs = self.getType(self.grid[yy][x])
                hexagon = Hexagon(
                    self.hex_radius,
                    bg_r,
                    bg_g,
                    bg_b,
                    bg_a,
                    stroke_r,
                    stroke_g,
                    stroke_b,
                    stroke_a,
                    stroke_thickness,
                    x,
                    y,
                    self.xRange,
                    self.yRange,
                    self.versus,
                    terrain = hex_attrs["terrain"],
                    color = hex_attrs["color"],
                    walkable=eval(hex_attrs["walkable"]),
                    showLabel=eval(hex_attrs["label"]),
                    fogOfWar=eval(hex_attrs["fogOfWar"])
                )
                if self.versus == HexGridType.HORIZONTAL:
                    hexagon.pos = (
                        x * (self.hex_innerRadius * 2)
                        + ((y + 1) % 2 * self.hex_innerRadius)
                        + center_x
                        - self.width / 2
                        - (self.hex_radius - self.hex_innerRadius),
                        (y * self.hex_radius * 1.5) + center_y - self.height / 2,
                    )
                else:
                    hexagon.pos = (
                        x * (self.hex_radius * 1.5) + center_x - self.width / 2,
                        y * (self.hex_innerRadius * 2)
                        + ((x + 1) % 2 * self.hex_innerRadius)
                        + center_y
                        - self.height / 2
                        - (self.hex_radius - self.hex_innerRadius),
                    )
                new_id = f"hex_{x}_{self.yRange - y -1}"
                self.ids[new_id] = hexagon
                self.add_widget(hexagon)
        pass

    def create_arrow(self):
        self.add_widget(self.arrow)
        pass

    def setArrow(self, hex, direction):
        self.ids[hex].setFogOfWar(False)
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
                    neibourghs = Contiguos.HORIZONTAL_GRID_EVEN_ROW_RANGE[even].copy()
                else:
                    # odd row
                    neibourghs = Contiguos.HORIZONTAL_GRID_EVEN_ROW_RANGE[odd].copy()
            else:
                # odd_r
                if parity_row == 0:
                    # even row
                    neibourghs = Contiguos.HORIZONTAL_GRID_ODD_ROW_RANGE[even].copy()
                else:
                    # odd row
                    neibourghs = Contiguos.HORIZONTAL_GRID_ODD_ROW_RANGE[odd].copy()
        else:
            # odd_q or even_q
            if xRange % 2 == 0:
                # even_q
                if parity_col == 0:
                    # even col
                    neibourghs = Contiguos.VERTICAL_GRID_EVEN_COL_RANGE[even].copy()
                else:
                    # odd col
                    neibourghs = Contiguos.VERTICAL_GRID_EVEN_COL_RANGE[odd].copy()
            else:
                # odd_q
                if parity_col == 0:
                    # even col
                    neibourghs = Contiguos.VERTICAL_GRID_ODD_COL_RANGE[even].copy()
                else:
                    # odd col
                    neibourghs = Contiguos.VERTICAL_GRID_ODD_COL_RANGE[odd].copy()
        return neibourghs

    def getPossibleHex(self, contiguos, direction):
        if direction == 0:
            clickable = [contiguos[5], contiguos[0], contiguos[1], contiguos[3]]
        elif direction == 1:
            clickable = [contiguos[0], contiguos[1], contiguos[2], contiguos[4]]
        elif direction == 2:
            clickable = [contiguos[1], contiguos[2], contiguos[3], contiguos[5]]
        elif direction == 3:
            clickable = [contiguos[2], contiguos[3], contiguos[4], contiguos[0]]
        elif direction == 4:
            clickable = [contiguos[3], contiguos[4], contiguos[5], contiguos[1]]
        else:
            clickable = [contiguos[4], contiguos[5], contiguos[0], contiguos[2]]
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
                elif cnt == 2:
                    newDirection = direction + 1
                    if newDirection > 5:
                        newDirection = 0
                    return f"rotate_{newDirection}"
                else:
                    return "move_back"
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
