from collections import namedtuple
from enum import Enum

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.relativelayout import RelativeLayout

from hexagon import Hexagon
from hexGridLayout import HexGridLayout


# Define an Enum for directions
class Direction(Enum):
    RIGHT = 0
    DOWN_RIGHT = 1
    DOWN_LEFT = 2
    LEFT = 3
    UP_LEFT = 4
    UP_RIGHT = 5


# Define a named tuple for the movement key
MovementKey = namedtuple("MovementKey", ["dif_x", "dif_y", "row_even", "yRangeEven"])

Config.set("graphics", "fullscreen", "auto")

from kivy.app import App


class HexApp(App):
    def build(self):
        self.hex_size = 100
        self.hex_height = self.hex_size * 0.866
        self.xRange = 15
        self.yRange = 10
        self.movements = {
            0: {
                (1, 0, 1, 1): "move",
                (1, 0, 1, 0): "move",
                (1, 0, 0, 1): "move",
                (1, 0, 0, 0): "move",
                (1, -1, 0, 1): "rotate_5",
                (0, -1, 1, 1): "rotate_5",
                (1, -1, 1, 0): "rotate_5",
                (0, -1, 0, 0): "rotate_5",
                (1, 1, 0, 1): "rotate_1",
                (0, 1, 1, 1): "rotate_1",
                (1, 1, 1, 0): "rotate_1",
                (0, 1, 0, 0): "rotate_1",
            },
            1: {
                (1, 1, 0, 1): "move",
                (0, 1, 1, 1): "move",
                (1, 1, 1, 0): "move",
                (0, 1, 0, 0): "move",
                (1, 0, 0, 1): "rotate_0",
                (1, 0, 1, 1): "rotate_0",
                (1, 0, 1, 0): "rotate_0",
                (1, 0, 0, 0): "rotate_0",
                (0, 1, 0, 1): "rotate_2",
                (-1, 1, 0, 0): "rotate_2",
                (-1, 1, 1, 1): "rotate_2",
                (0, 1, 1, 0): "rotate_2",
            },
            2: {
                (0, 1, 0, 1): "move",
                (-1, 1, 1, 1): "move",
                (-1, 1, 0, 0): "move",
                (0, 1, 1, 0): "move",
                (0, 1, 1, 1): "rotate_1",
                (1, 1, 0, 1): "rotate_1",
                (1, 1, 1, 0): "rotate_1",
                (0, 1, 0, 0): "rotate_1",
                (-1, 0, 0, 1): "rotate_3",
                (-1, 0, 1, 1): "rotate_3",
                (-1, 0, 1, 0): "rotate_3",
                (-1, 0, 0, 0): "rotate_3",
            },
            3: {
                (-1, 0, 0, 1): "move",
                (-1, 0, 1, 1): "move",
                (-1, 0, 1, 0): "move",
                (-1, 0, 0, 0): "move",
                (0, 1, 0, 1): "rotate_2",
                (-1, 1, 1, 1): "rotate_2",
                (0, 1, 1, 0): "rotate_2",
                (-1, 1, 0, 0): "rotate_2",
                (0, -1, 0, 1): "rotate_4",
                (-1, -1, 1, 1): "rotate_4",
                (0, -1, 1, 0): "rotate_4",
                (-1, -1, 0, 0): "rotate_4",
            },
            4: {
                (0, -1, 0, 1): "move",
                (-1, -1, 1, 1): "move",
                (-1, -1, 0, 0): "move",
                (0, -1, 1, 0): "move",
                (-1, 0, 0, 1): "rotate_3",
                (-1, 0, 1, 1): "rotate_3",
                (-1, 0, 1, 0): "rotate_3",
                (-1, 0, 0, 0): "rotate_3",
                (1, -1, 0, 1): "rotate_5",
                (0, -1, 1, 1): "rotate_5",
                (1, -1, 1, 0): "rotate_5",
                (0, -1, 0, 0): "rotate_5",
            },
            5: {
                (1, -1, 0, 1): "move",
                (0, -1, 1, 1): "move",
                (1, -1, 1, 0): "move",
                (0, -1, 0, 0): "move",
                (0, -1, 0, 1): "rotate_4",
                (-1, -1, 1, 1): "rotate_4",
                (0, -1, 1, 0): "rotate_4",
                (-1, -1, 0, 0): "rotate_4",
                (1, 0, 0, 1): "rotate_0",
                (1, 0, 1, 1): "rotate_0",
                (1, 0, 1, 0): "rotate_0",
                (1, 0, 0, 0): "rotate_0",
            },
        }
        Window.maximize()
        self.container = RelativeLayout()

        # Create an instance of HexGridLayout with appropriate parameters
        self.grid = HexGridLayout(
            hex_size=self.hex_size, xRange=self.xRange, yRange=self.yRange
        )

        self.grid.size_hint = (None, None)
        self.grid.size = (
            self.hex_height * (self.xRange * 2 + 1),
            self.hex_size * (self.yRange * 1.5)
            + (self.hex_height - (self.hex_height * 0.866 / 2)),
        )
        self.grid.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.container.add_widget(self.grid)
        return self.container

    def hexClicked_handler(self, instance):
        arrow_x, arrow_y, arrow_direction = self.grid.getArrow()
        dif_x = instance.xCoord - arrow_x
        dif_y = instance.yCoord - arrow_y
        row_even = arrow_y % 2
        yRangeEven = self.yRange % 2

        movement_key = MovementKey(dif_x, dif_y, row_even, yRangeEven)

        # Check if clicked hex is the one with the arrow
        if dif_x == 0 and dif_y == 0:
            return

        # Conditions for contiguous hexes
        if movement_key in self.get_contiguous_hexes():
            action = self.movements[arrow_direction].get(movement_key)
            if action is None:
                # Log error or print
                return
            self.perform_action(action, instance)
        else:
            # Log error or print
            return

    def perform_action(self, action, instance):
        if action == "move":
            self.grid.moveArrow(instance.name)
        elif action.startswith("rotate_"):
            self.grid.rotateArrow(int(action.split("_")[-1]))

    def get_contiguous_hexes(self):
        # All possible contiguous movements for both even and odd rows
        contiguous_movements = [
            MovementKey(-1, -1, 0, 0),
            MovementKey(-1, -1, 0, 1),
            MovementKey(-1, -1, 1, 1),
            MovementKey(-1, 0, 0, 0),
            MovementKey(-1, 0, 0, 1),
            MovementKey(-1, 0, 1, 0),
            MovementKey(-1, 0, 1, 1),            
            MovementKey(-1, 1, 0, 0),
            MovementKey(-1, 1, 0, 1),
            MovementKey(-1, 1, 1, 1),
            MovementKey(0, -1, 0, 0),
            MovementKey(0, -1, 0, 1),
            MovementKey(0, -1, 1, 0),
            MovementKey(0, -1, 1, 1),
            MovementKey(0, 1, 0, 0),
            MovementKey(0, 1, 0, 1),
            MovementKey(0, 1, 1, 0),
            MovementKey(0, 1, 1, 1),
            MovementKey(1, -1, 0, 1),
            MovementKey(1, -1, 1, 0),
            MovementKey(1, -1, 1, 1),
            MovementKey(1, 0, 0, 0),
            MovementKey(1, 0, 0, 1),
            MovementKey(1, 0, 1, 0),
            MovementKey(1, 0, 1, 1),
            MovementKey(1, 1, 0, 1),
            MovementKey(1, 1, 1, 0),
            MovementKey(1, 1, 1, 1),
        ]
        return contiguous_movements

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
