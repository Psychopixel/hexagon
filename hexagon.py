from math import cos, pi, sin

from kivy.core.image import Image
from kivy.graphics import Color, Line, Mesh, PopMatrix, PushMatrix, Rectangle, Rotate
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout

from definition import *

F_HEX = 0.866


class Hexagon(RelativeLayout):
    def __init__(
        self,
        hex_size,
        bg_r,
        bg_g,
        bg_b,
        bg_a,
        stroke_r,
        stroke_g,
        stroke_b,
        stroke_a,
        stroke_tickness,
        x,
        y,
        xRange,
        yRange,
        versus,
        terrain=None,
        color=None,
        walkable=True,
        showLabel=True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.hex_size = hex_size
        self.r = bg_r
        self.g = bg_g
        self.b = bg_b
        self.a = bg_a
        self.stroke_r = stroke_r
        self.stroke_g = stroke_g
        self.stroke_b = stroke_b
        self.stroke_a = stroke_a
        self.stroke_tickness = stroke_tickness

        self.xRange = xRange
        self.yRange = yRange
        self.versus = versus
        self.xCoord = x
        self.yCoord = self.yRange - y - 1

        self.terrain = terrain
        self.hex_color = color if color else (bg_r, bg_g, bg_b, bg_a)
        self.walkable = walkable
        self.texture = None
        if self.terrain:
            # Load the image into a texture
            self.texture = Image(f".\images\{self.terrain}").texture
            # Ensure the texture repeats instead of stretching
            self.texture.wrap = "repeat"
        self.showLabel=showLabel

        self.coords_label = Label()
        self.coords_label.color = (1, 1, 1, 1)
        self.size_hint = (None, None)
        self.hex_height = self.hex_size * 0.866
        self.size = (self.hex_size, self.hex_height)
        # Bind label to update whenever x or y changes
        self.bind(x=self.update_label, y=self.update_label)
        self.redraw()
        if self.showLabel:
            self.add_widget(self.coords_label)

        # Register the custom event
        self.register_event_type("on_hex_clicked_event")

    def update_label(self, instance, value):
        self.coords_label.text = f"({self.xCoord}, {self.yCoord})"
        self.coords_label.pos = (self.hex_size / 2, self.hex_size / 2)
        self.name = f"hex_{self.xCoord}_{self.yCoord}"

    def convert_to_kivy_color(self, rgba):
        r, g, b, a = rgba
        return r / 255.0, g / 255.0, b / 255.0, a

    def redraw(self):
        with self.canvas.before:
            self.canvas.clear()
            # Using self.hex_color to set the color for drawing
            r, g, b, a = self.convert_to_kivy_color(self.hex_color)
            Color(r, g, b, a)

            triangleVertices, self.vertices, indices = self.build_mesh(
                rotation=self.versus
            )

            mesh = Mesh(vertices=triangleVertices, indices=indices)
            mesh.mode = "triangle_fan"
            if self.stroke_tickness > 0:
                Color(self.stroke_r, self.stroke_g, self.stroke_b, self.stroke_a)
                Line(points=self.vertices, width=self.stroke_tickness)
            # Draw the image (if provided) inside the hexagon
            if self.texture:
                # The scaling factor ensures the image fits inside the hexagon
                scale_factor = (
                    self.hex_size * 2.0 / max(self.texture.width, self.texture.height)
                )
                scaled_width = self.texture.width * scale_factor
                scaled_height = self.texture.height * scale_factor
                # Positioning the image
                pos_x = 0
                pos_y = 14
                Color(1, 1, 1, 1)  # Reset to white color for the image

                if self.versus == HexGridType.HORIZONTAL:
                    # Use PushMatrix to remember the current graphics state
                    PushMatrix()
                    # Rotate the texture by 90 degrees
                    Rotate(
                        angle=-90,
                        origin=(pos_x + scaled_width / 2, pos_y + scaled_height / 2),
                    )

                Rectangle(
                    pos=(pos_x, pos_y),
                    size=(scaled_width, scaled_height),
                    texture=self.texture,
                )

                if self.versus == HexGridType.HORIZONTAL:
                    # Restore the original graphics state
                    PopMatrix()

    def point_inside_parallelogram(self, point, v1, v2, v3, v4):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        d1 = sign(point, v1, v2)
        d2 = sign(point, v2, v3)
        d3 = sign(point, v3, v4)
        d4 = sign(point, v4, v1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0) or (d4 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0) or (d4 > 0)

        return not (has_neg and has_pos)

    def on_touch_down(self, touch):
        # Check if the touch event occurred within this widget
        self.v1 = [self.vertices[0] + self.pos[0], self.vertices[1] + self.pos[1]]
        self.v2 = [self.vertices[2] + self.pos[0], self.vertices[3] + self.pos[1]]
        self.v3 = [self.vertices[4] + self.pos[0], self.vertices[5] + self.pos[1]]
        self.v4 = [self.vertices[6] + self.pos[0], self.vertices[7] + self.pos[1]]
        self.v5 = [self.vertices[8] + self.pos[0], self.vertices[9] + self.pos[1]]
        self.v6 = [self.vertices[10] + self.pos[0], self.vertices[11] + self.pos[1]]

        point = list(touch.pos)
        if (
            self.point_inside_parallelogram(point, self.v1, self.v2, self.v4, self.v5)
            or self.point_inside_parallelogram(
                point, self.v2, self.v3, self.v5, self.v6
            )
            or self.point_inside_parallelogram(
                point, self.v3, self.v4, self.v6, self.v1
            )
        ):
            # Dispatch the custom event
            self.dispatch("on_hex_clicked_event")

            # Handle the event and stop propagation
            return True

        # If the touch event wasn't within this widget, continue propagation
        return super().on_touch_down(touch)

    def on_hex_clicked_event(self, *args):
        # Set the bubbled property to True to propagate the event
        pass

    def build_mesh(self, rotation=0.0):
        # returns a Mesh of a rough circle with rotation.
        vertices = []
        triangleVertices = []
        indices = []
        step = 6
        istep = (pi * 2) / float(step)

        # Center point of the circle
        triangleVertices.extend([self.hex_size, self.hex_size, 0, 0])

        # Generating circle points with rotation
        for i in range(step):
            x = cos(istep * i + rotation) * self.hex_size
            y = sin(istep * i + rotation) * self.hex_size
            vertices.append(self.hex_size + x)
            vertices.append(self.hex_size + y)
            # Add the x and y coordinates relative to the center point
            triangleVertices.extend([self.hex_size + x, self.hex_size + y, 0, 0])
        vertices.append(vertices[0])
        vertices.append(vertices[1])

        # Generating indices for triangles
        for i in range(1, step):
            indices.extend([0, i, i + 1])
        indices.extend([0, step, 1])  # to close the circle

        return triangleVertices, vertices, indices

    def get_attributes(self):
        # Retrieve the attributes of the hexagon.
        return {
            "terrain": self.terrain,
            "color": self.hex_color,
            "walkable": self.walkable,
        }

    def set_attributes(self, terrain=None, color=None, walkable=None):
        # Modify the attributes of the hexagon.
        if terrain:
            self.terrain = terrain
        if color:
            self.hex_color = color
            self.r, self.g, self.b, self.a = color  # Update the hexagon's display color
            self.redraw()  # Redraw the hexagon with the new color
        if walkable:
            self.walkable = walkable
