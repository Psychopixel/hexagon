
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
        self.xCoord = x
        self.yCoord = y
        self.xRange = xRange
        self.yRange = yRange

        self.coords_label = Label()
        self.coords_label.color = (1,1,1,1)
        self.size_hint = (None, None)
        self.hex_height = self.hex_size * 0.866
        self.size = (self.hex_size, self.hex_height)
        # Bind label to update whenever x or y changes
        self.bind(x=self.update_label, y=self.update_label)
        self.redraw()
        self.add_widget(self.coords_label)

    def update_label(self, instance, value):
        self.coords_label.text = f"({self.xCoord}, {self.yRange - self.yCoord -1})"
        self.coords_label.pos = (self.hex_size/2, self.hex_size/2)

    def redraw(self):
        with self.canvas.before:
            self.canvas.clear()
            Color(self.r, self.g, self.b, self.a)
            triangleVertices, vertices, indices = self.build_mesh(pi/2)
            mesh = Mesh(vertices=triangleVertices, indices=indices)
            mesh.mode = "triangle_fan"
            if self.stroke_tickness>0:
                Color(self.stroke_r, self.stroke_g, self.stroke_b, self.stroke_a)
                Line(points=vertices, width=self.stroke_tickness)

    def on_touch_down(self, touch):
        # Check if the touch event occurred within this widget
        if self.collide_point(*touch.pos):
            print("Hex " + self.coords_label.text + " was touched!")
            
            # Handle the event and stop propagation
            return True
        
        # If the touch event wasn't within this widget, continue propagation
        return super(Hexagon, self).on_touch_down(touch)

    
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
