import json

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.relativelayout import RelativeLayout

from definition import *
from hexGridLayout import HexGridLayout
from hexagon import Hexagon

Config.set("graphics", "fullscreen", "auto")

from kivy.app import App

class HexApp(App):
    def build(self):
        map_data = self.load_map_data()
        self.map_attrs = map_data.get("map", {})
        if self.map_attrs:
            self.hex_radius = self.map_attrs.get("hex_radius", 75)
            self.xRange = self.map_attrs.get("xRange", 10)
            self.yRange = self.map_attrs.get("yRange", 10)
            orientation = self.map_attrs.get("orientation", "VERTICAL")
            if orientation == "VERTICAL":
                self.versus = HexGridType.VERTICAL
            else:
                self.versus = HexGridType.HORIZONTAL
        else:
            self.hex_radius = 100
            self.xRange = 10
            self.yRange = 10
            self.versus = HexGridType.VERTICAL

        self.hex_innerRadius = self.hex_radius * F_HEX

        Window.maximize()
        self.container = RelativeLayout()

        # Create an instance of HexGridLayout with appropriate parameters
        self.grid = HexGridLayout(
            hex_radius=self.hex_radius,
            xRange=self.xRange,
            yRange=self.yRange,
            versus=self.versus,
        )

        self.grid.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.container.add_widget(self.grid)
        return self.container

    def load_map_data(self, filename="map_data.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            return data
        except Exception as e:
            print(f"Error loading map data: {e}")
            return {}

    def hexClicked_handler(self, instance:Hexagon):
        move = self.grid.calculateMove(instance)
        if move == None:
            return
        instance.setFogOfWar(False)
        if not instance.walkable and (move == "move" or move == "move_back"):
            return
        else:
            self.perform_action(move, instance)

    def perform_action(self, action, instance):
        if action == "move" or action == "move_back":
            self.grid.moveArrow(instance.name)
        elif action.startswith("rotate_"):
            self.grid.rotateArrow(int(action.split("_")[-1]))

    def on_start(self):
        self.container.center = Window.center
        self.grid.create_hex(
            self.container.center_x, self.container.center_y, hex_data={}
        )
        for hex in self.grid.children:
            hex.bind(on_hex_clicked_event=self.hexClicked_handler)
        self.grid.create_arrow()
        start_hex = self.map_attrs.get("start_hex", "hex_5_5")
        start_direction = self.map_attrs.get("start_direction", 0)
        r, g, b, a = self.map_attrs.get("backgroundColor", [0.15, 0.15, 0.15, 1])
        self.grid.setArrow(start_hex, start_direction)
        # app background color
        self.coloraSfondo(self.root, r, g, b, a)

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
