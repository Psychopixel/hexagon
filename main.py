from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.relativelayout import RelativeLayout

from hexagon import Hexagon
from hexGridLayout import HexGridLayout

Config.set("graphics", "fullscreen", "auto")

from kivy.app import App


class HexApp(App):
    def build(self):
        self.hex_size = 100
        self.hex_height = self.hex_size * 0.866
        self.xRange = 10
        self.yRange = 10
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

        # Define possible movements based on direction and differences
        movements = {
            0: {
                (1, 0, 1): 'move',
                (1, 0, 0): 'move',
                (0, -1, 0): 'rotate_5',
                (1, -1, 1): 'rotate_5',
                (0, 1, 0): 'rotate_1',
                (1, 1, 1): 'rotate_1'
            },
            1: {
                (0, 1, 0): 'move',
                (1, 1, 1): 'move',
                (1, 0, 0): 'rotate_0',
                (1, 0, 1): 'rotate_0',
                (-1, 1, 0): 'rotate_2',
                (0, 1, 1): 'rotate_2'
            },
            2: {
                (-1, 1, 0): 'move',
                (0, 1, 1): 'move',
                (0, 1, 0): 'rotate_1',
                (1, 1, 1): 'rotate_1',
                (-1, 0, 0): 'rotate_3',
                (-1, 0, 1): 'rotate_3'
            },
            3: {
                (-1, 0, 0): 'move',
                (-1, 0, 1): 'move',
                (-1, 1, 0): 'rotate_2',
                (0, 1, 1): 'rotate_2',
                (-1, -1, 0): 'rotate_4',
                (0, -1, 1): 'rotate_4',
            },
            4: {
                (-1, -1, 0): 'move',
                (0, -1, 1): 'move',
                (-1, 0, 0): 'rotate_3',
                (-1, 0, 1): 'rotate_3',
                (0, -1, 0): 'rotate_5',
                (1, -1, 1): 'rotate_5'
            },
            5: {
                (0, -1, 0): 'move',
                (1, -1, 1): 'move',
                (-1, -1, 0): 'rotate_4',
                (0, -1, 1): 'rotate_4',
                (1, 0, 0): 'rotate_0',
                (1, 0, 1): 'rotate_0'
            }
        }

        # Check if clicked hex is the one with the arrow
        if dif_x == 0 and dif_y == 0:
            return

        # Conditions for contiguous hexes
        if arrow_y % 2 == 0:  # Even row
            if (dif_x, dif_y, 0) in [(-1, 0, 0), (-1, 1, 0), (0, 1, 0), (-1, -1, 0), (0, -1, 0), (1, 1, 0), (1, 0, 0) ]:
                action = movements[arrow_direction].get((dif_x, dif_y, 0))
            else:
                return
        else:  # Odd row
            if (dif_x, dif_y, 1) in [(1, 0, 1), (1, -1, 1), (0, 1, 1), (1, 1, 1), (-1, 0, 1), (0, -1, 1)]:
                action = movements[arrow_direction].get((dif_x, dif_y, 1))
            else:
                return
        if action == None:
            print(f"Errore! dif_x: {dif_x} dif_y: {dif_y} direction: {arrow_direction} y_coord: {arrow_y} ")
        else:
            # Perform the appropriate action based on the direction and differences
            if action == 'move':
                self.grid.moveArrow(instance.name)
            elif action.startswith('rotate_'):
                self.grid.rotateArrow(int(action.split('_')[-1]))


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
