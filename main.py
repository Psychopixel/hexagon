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
        self.grid = HexGridLayout(hex_size=self.hex_size, xRange=self.xRange, yRange=self.yRange)

        self.grid.size_hint = (None, None)
        self.grid.size = (
            self.hex_height * (self.xRange * 2 + 1),
            self.hex_size * (self.yRange * 1.5)
            + (self.hex_height - (self.hex_height * 0.866 / 2)),
        )
        self.grid.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.container.add_widget(self.grid)

        return self.container

    def on_start(self):
        self.container.center = Window.center
        self.grid.create_hex(self.container.center_x, self.container.center_y)
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
