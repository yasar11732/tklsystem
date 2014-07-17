from __future__ import division

import tkinter as tk

from PIL import Image, ImageTk
from PIL.ImageDraw import ImageDraw

from l_system_utils import PlaceHolder

import tempfile
from os.path import join, isdir, isfile
from os import makedirs

import hashlib

image_cache_dir = join(tempfile.gettempdir(), "lsd_pil_images")
    
class TurtleCanvas(tk.Canvas):

    "Draw directly on tkinter canvas"
    def draw_turtle(self, turtle, colors={}): # no need to overwrite parent's init

        if self.load_from_cache(turtle.string):
            return

        c_width = int(self['width'])
        c_height = int(self['height'])
        
        self.pil_image = Image.new("RGB", (c_width, c_height), (255,255,255))
        im_draw = ImageDraw(self.pil_image)

        color = "#000000" # default color

        # Calculate size, and scale to fill the frame
        t_width = turtle.rightmost[0] - turtle.leftmost[0]
        t_height = turtle.bottommost[1] - turtle.topmost[1]

        if t_width / t_height > 1: # fat image scale according to width
            scale_factor = c_width / t_width
        else:
            scale_factor = c_height / t_height


        left_margin = (c_width - scale_factor*t_width)  / 2
        top_margin  = (c_height - scale_factor*t_height) / 2

        x_shift = left_margin - scale_factor*turtle.leftmost[0]
        y_shift = top_margin  - scale_factor*turtle.topmost[1]
        
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
                im_draw.line(item, color)

        self.photo_image = ImageTk.PhotoImage(self.pil_image)
        self.delete('all')

        self.create_image((c_width/2, c_height/2), image=self.photo_image)

        self.save_to_cache(turtle.string)

    def load_from_cache(self, string):

        m = hashlib.sha256()
        m.update(string.encode('utf-8'))

        filename = join(image_cache_dir, m.hexdigest() + ".jpg")

        if not isfile(filename):
            return False

        self.pil_image = Image.open(filename)
        self.photo_image = ImageTk.PhotoImage(self.pil_image)
        self.delete('all')

        self.create_image((int(self['width'])/2, int(self['height'])/2), image=self.photo_image)
        return True

    
    def save_to_cache(self, string):
        
        m = hashlib.sha256()
        m.update(string.encode('utf-8'))

        filename = join(image_cache_dir, m.hexdigest() + ".jpg")

        if not isdir(image_cache_dir):
            makedirs(image_cache_dir)
            
        self.pil_image.save(filename)
        
