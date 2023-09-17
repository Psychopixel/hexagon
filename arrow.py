from math import pi
import os
from kivy.graphics import Color, Rectangle, Rotate
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout

from definition import HexGridType, AppPath

class Arrow(RelativeLayout):
    def __init__(self, versus, **kwargs):
        super().__init__(**kwargs)
        self.versus = versus

        # Construct the path in a cross-platform way
        path = os.path.join(AppPath.resource_path("images"))
        self.arrow_button = Button(
            background_normal=os.path.join(path, "freccia.png"),
            background_down=os.path.join(path, "freccia.png"),
            size_hint=(None, None),
        )
        self.arrow_button.pos_hint = ({"center_x": 0.5, "center_y": 0.5})
        # Add the button to the Arrow layout
        self.add_widget(self.arrow_button)
        #self.coloraSfondo(self.arrow_button, 1., 0.15, 0.15, 1)
        self.size=self.arrow_button.size
        self.xCoord = -1
        self.yCoord = -1
        self.direction = 0
        if self.versus == HexGridType.VERTICAL:
            with self.arrow_button.canvas.before:
                # Apply the rotation
                Rotate(angle=-30, origin=self.arrow_button.center)

    def moveArrow(self, center, xCoord, yCoord):
        self.center = center
        # XXXXXXXXXXXXXXXXXX
        # this is a correction to be eliminated
        self.x -= 12.5
        self.y -= 7.5
        # ------------------------------
        self.xCoord = xCoord
        self.yCoord = yCoord

    def rotateButton(self, direction):
        # Apply the rotation
        if direction != self.direction:
            angleRotation = (self.direction - direction) * 60
            # Apply a rotation of 45 degrees about the center of the widget
            with self.arrow_button.canvas.before:
                # Apply the rotation
                Rotate(angle=angleRotation, origin=self.arrow_button.center)
            self.direction = direction
            pass

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
