
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.graphics import Rotate
from math import pi

class Arrow(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create a button with the image texture
        self.arrow_button = Button(background_normal='freccia.png', background_down='freccia.png', size_hint=(None, None), )
        
        # Add the button to the Arrow layout
        self.add_widget(self.arrow_button)
        #self.coloraSfondo(self.arrow_button, 1., 0.15, 0.15, 1)


    def rotateButton(self, direction):
        # Apply the rotation
        angleRotation = direction * -60
        # Apply a rotation of 45 degrees about the center of the widget
        with self.arrow_button.canvas.before:
           
            # Apply the rotation
            Rotate(angle=angleRotation, origin=self.arrow_button.center)
            
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
