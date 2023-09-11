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
        print(
            f"Received on_hex_clicked_event in {self.__class__.__name__} from {str(instance.xCoord)}, {str(instance.yCoord)}!"
        )
        arrow_x, arrow_y, arrow_direction = self.grid.getArrow()
        print(
            f"La freccia si trova sull'hex ({arrow_x},{arrow_y}) direzione: {arrow_direction}"
        )
        dif_x = instance.xCoord - arrow_x
        dif_y = instance.yCoord - arrow_y
        print(f"dif_x: {dif_x} dif_y: {dif_y}")

        if dif_x == 0 and dif_y == 0:
            # hex della freccia
            pass
        else:
            # hex contiguous
            if arrow_y % 2 == 0:
                # row even
                if dif_x > 1 or dif_x < -1 or dif_y > 1 or dif_y < -1:
                    # hex not contiguous
                    pass
                elif not (
                    (dif_x == -1 and dif_y == -1)
                    or (dif_x == 0 and dif_y == -1)
                    or (dif_x == 1 and dif_y == 0)
                    or (dif_x == 0 and dif_y == 1)
                    or (dif_x == -1 and dif_y == 1)
                    or (dif_x == -1 and dif_y == 0)
                ):
                    # hex not contiguous
                    pass
                else:
                    if arrow_direction == 0:
                        if dif_x == 1 and dif_y == 0:
                            self.grid.moveArrow(instance.name)
                        elif dif_x == 0 and dif_y == -1:
                            self.grid.rotateArrow(5)
                        elif dif_x == 0 and dif_y == 1:
                            self.grid.rotateArrow(1)
                    elif arrow_direction == 1:
                        if dif_x == 0 and dif_y == 1:
                            self.grid.moveArrow(instance.name)
                        elif dif_x == 1 and dif_y == 0:
                            self.grid.rotateArrow(0)
                        elif dif_x == -1 and dif_y == 1:
                            self.grid.rotateArrow(2)
                    elif arrow_direction == 2:
                        if dif_x == -1 and dif_y == 1:
                            self.grid.moveArrow(instance.name)
                        elif dif_x == 0 and dif_y == 1:
                            self.grid.rotateArrow(1)
                        elif dif_x == -1 and dif_y == 0:
                            self.grid.rotateArrow(3)
                    elif arrow_direction == 3:
                        if dif_x == -1 and dif_y == 0:
                            self.grid.moveArrow(instance.name)
                        elif dif_x == -1 and dif_y == 1:
                            self.grid.rotateArrow(2)
                        elif dif_x == -1 and dif_y == -1:
                            self.grid.rotateArrow(4)
                    elif arrow_direction == 4:
                        if dif_x == -1 and dif_y == -1:
                            self.grid.moveArrow(instance.name)
                        elif dif_x == -1 and dif_y == 0:
                            self.grid.rotateArrow(3)
                        elif dif_x == 0 and dif_y == -1:
                            self.grid.rotateArrow(5)
                    else:
                        if dif_x == 0 and dif_y == -1:
                            self.grid.moveArrow(instance.name)
                        elif dif_x == -1 and dif_y == -1:
                            self.grid.rotateArrow(4)
                        elif dif_x == 1 and dif_y == 0:
                            self.grid.rotateArrow(0)
            else:
                # row odd
                if dif_x > 1 or dif_x < -1 or dif_y > 1 or dif_y < -1:
                    # hex not contiguous
                    pass
                elif (dif_x == -1 and dif_y == -1) or (dif_x == -1 and dif_y == 1):
                    # hex not contiguous
                    pass
                else:
                    if arrow_direction == 0:
                        if dif_x == 1 and dif_y == 0:
                            self.grid.moveArrow(instance.name)
                        elif dif_x == 1 and dif_y == -1:
                            self.grid.rotateArrow(5)
                        elif dif_x == 1 and dif_y == 1:
                            self.grid.rotateArrow(1)
                    elif arrow_direction == 1:
                        if dif_x == 1 and dif_y == 1:
                            self.grid.moveArrow(instance.name)
                        elif dif_x == 1 and dif_y == 0:
                            self.grid.rotateArrow(0)
                        elif dif_x == 0 and dif_y == 1:
                            self.grid.rotateArrow(2)
                    elif arrow_direction == 2:
                        if dif_x == 0 and dif_y == 1:
                            self.grid.moveArrow(instance.name)
                        elif dif_x == 1 and dif_y == 1:
                            self.grid.rotateArrow(1)
                        elif dif_x == -1 and dif_y == 0:
                            self.grid.rotateArrow(3)
                    elif arrow_direction == 3:
                        if dif_x == -1 and dif_y == 0:
                            self.grid.moveArrow(instance.name)
                        elif dif_x == 0 and dif_y == 1:
                            self.grid.rotateArrow(2)
                        elif dif_x == 0 and dif_y == -1:
                            self.grid.rotateArrow(4)
                    elif arrow_direction == 4:
                        if dif_x == 0 and dif_y == -1:
                            self.grid.moveArrow(instance.name)
                        elif dif_x == -1 and dif_y == 0:
                            self.grid.rotateArrow(3)
                        elif dif_x == 1 and dif_y == -1:
                            self.grid.rotateArrow(5)
                    else:
                        if dif_x == 1 and dif_y == -1:
                            self.grid.moveArrow(instance.name)
                        elif dif_x == 0 and dif_y == -1:
                            self.grid.rotateArrow(4)
                        elif dif_x == 1 and dif_y == 0:
                            self.grid.rotateArrow(0)

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
