from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.relativelayout import RelativeLayout

from definition import *
from hexGridLayout import HexGridLayout

Config.set("graphics", "fullscreen", "auto")

from kivy.app import App


class HexApp(App):
    def build(self):
        self.hex_size = 100
        self.hex_height = self.hex_size * 0.866
        self.xRange = 9
        self.yRange = 10

        Window.maximize()
        self.container = RelativeLayout()

        # Create an instance of HexGridLayout with appropriate parameters
        self.grid = HexGridLayout(
            hex_size=self.hex_size,
            xRange=self.xRange,
            yRange=self.yRange,
            versus=HexGridType.VERTICAL,
        )

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

        self.grid.size_hint = (None, None)
        self.grid.size = (
            self.hex_height * (self.xRange * 2 + 1),
            self.hex_size * (self.yRange * 1.5)
            + (self.hex_height - (self.hex_height * 0.866 / 2)),
        )
        self.grid.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.container.add_widget(self.grid)
        return self.container

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

    def hexClicked_handler(self, instance):
        arrow_x, arrow_y, arrow_direction = self.grid.getArrow()

        move = self.getMove(
            self.getPossibleHex(
                self.getAllContiguos(
                    yRange=self.yRange,
                    xRange=self.xRange,
                    arrow_x=arrow_x,
                    arrow_y=arrow_y,
                    gridVersus=self.grid.versus,
                ),
                direction=arrow_direction,
            ),
            [instance.xCoord, instance.yCoord],
            arrow_x=arrow_x,
            arrow_y=arrow_y,
            direction=arrow_direction,
        )
        if move == None:
            return
        else:
            self.perform_action(move, instance)

    def perform_action(self, action, instance):
        if action == "move":
            self.grid.moveArrow(instance.name)
        elif action.startswith("rotate_"):
            self.grid.rotateArrow(int(action.split("_")[-1]))

    def on_start(self):
        self.container.center = Window.center
        self.grid.create_hex(self.container.center_x, self.container.center_y)
        for hex in self.grid.children:
            hex.bind(on_hex_clicked_event=self.hexClicked_handler)
        self.grid.create_arrow()
        self.grid.setArrow("hex_5_5", 0)
        # app background color
        self.coloraSfondo(self.root, 0.15, 0.15, 0.15, 1)

        return super().on_start()

    def coloraSfondo(self, layout, r, g, b, a):
        with layout.canvas.before:
            Color(r, g, b, a)
            # Update the rectangle position and size when the layout changes
            layout.bind(pos=self.update_rect, size=self.update_rect)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

    def update_bg_pos(self, instance, value):
        self.bg.pos = instance.pos

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == "__main__":
    HexApp().run()
