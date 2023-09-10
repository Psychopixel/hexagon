
from math import cos, pi, sin

from kivy.graphics import Color, Line, Mesh
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout

F_HEX = 0.866

class Hexagon(RelativeLayout):

    def __init__(self, hex_size, bg_r, bg_g, bg_b, bg_a, stroke_r, stroke_g, stroke_b, stroke_a, stroke_tickness, x, y, xRange, yRange, **kwargs):
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
        self.xCoord = x
        self.yCoord = self.yRange - y - 1

        self.coords_label = Label()
        self.coords_label.color = (1,1,1,1)
        self.size_hint = (None, None)
        self.hex_height = self.hex_size * 0.866
        self.size = (self.hex_size, self.hex_height)
        # Bind label to update whenever x or y changes
        self.bind(x=self.update_label, y=self.update_label)
        self.redraw()
        self.add_widget(self.coords_label)

        # Register the custom event
        self.register_event_type('on_hex_clicked_event')

    def update_label(self, instance, value):
        self.coords_label.text = f"({self.xCoord}, {self.yCoord})"
        self.coords_label.pos = (self.hex_size/2, self.hex_size/2)

    def redraw(self):
        with self.canvas.before:
            self.canvas.clear()
            Color(self.r, self.g, self.b, self.a)
            triangleVertices, self.vertices, indices = self.build_mesh(pi/2)
            
            mesh = Mesh(vertices=triangleVertices, indices=indices)
            mesh.mode = "triangle_fan"
            if self.stroke_tickness>0:
                Color(self.stroke_r, self.stroke_g, self.stroke_b, self.stroke_a)
                Line(points=self.vertices, width=self.stroke_tickness)
            

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
        if self.point_inside_parallelogram(point, self.v1, self.v2, self.v4, self.v5) \
            or self.point_inside_parallelogram(point, self.v2, self.v3, self.v5, self.v6) \
                or self.point_inside_parallelogram(point, self.v3, self.v4, self.v6, self.v1):
            print("Hex " + self.coords_label.text + " was touched!")
            # Dispatch the custom event
            self.dispatch('on_hex_clicked_event')
            
            # Handle the event and stop propagation
            return True
        
        # If the touch event wasn't within this widget, continue propagation
        return super().on_touch_down(touch)

    def on_hex_clicked_event(self, *args):
        # Set the bubbled property to True to propagate the event
        self.bubbled = True
        print(f"{self.coords_label.text} dispatched on_hex_clicked_event!")
    
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
            vertices.append( self.hex_size + y)
            # Add the x and y coordinates relative to the center point
            triangleVertices.extend([self.hex_size + x, self.hex_size + y, 0, 0])
        vertices.append(vertices[0])
        vertices.append(vertices[1])

        # Generating indices for triangles
        for i in range(1, step):
            indices.extend([0, i, i+1])
        indices.extend([0, step, 1])  # to close the circle

        return triangleVertices, vertices, indices
