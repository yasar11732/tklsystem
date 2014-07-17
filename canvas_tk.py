from __future__ import division

import tkinter as tk
from l_system_utils import PlaceHolder
    
class TurtleCanvas(tk.Canvas):

    "Draw directly on tkinter canvas"
    def draw_turtle(self, turtle, colors={}): # no need to overwrite parent's init
        color = "#000000" # default color

        # Calculate size, and scale to fill the frame
        print("{}, {}, {}, {}".format(turtle.leftmost, turtle.topmost, turtle.rightmost,turtle.bottommost))
        t_width = turtle.rightmost[0] - turtle.leftmost[0]
        t_height = turtle.bottommost[1] - turtle.topmost[1]
        print("Turtle widht", t_width, "Turtle height", t_height)

        c_width = int(self['width'])
        c_height = int(self['height'])
        print("Canvas width", c_width, "Canvas height", c_height)

        if t_width / t_height > 1: # fat image scale according to width
            scale_factor = c_width / t_width
        else:
            scale_factor = c_height / t_height

        print("scale factor", scale_factor)


        left_margin = (c_width - scale_factor*t_width)  / 2
        top_margin  = (c_height - scale_factor*t_height) / 2

        x_shift = left_margin - scale_factor*turtle.leftmost[0]
        y_shift = top_margin  - scale_factor*turtle.topmost[1]

        print("x_shift", x_shift, "y_shift", y_shift)
        
        coordinates = []

        for item in turtle.lines:
            if isinstance(item, PlaceHolder):
                coordinates.append(item)
            else:
                coordinates.append((item[0]*scale_factor+x_shift,
                                    item[1]*scale_factor+y_shift,
                                    item[2]*scale_factor+x_shift,
                                    item[3]*scale_factor+y_shift))
            
        for item in coordinates:
            if isinstance(item, PlaceHolder): # not a list of coordinates
                if item.value in colors:
                    color = colors[item.value]
            else:
                self.create_line(*item, fill=color)






    

        
        
        
