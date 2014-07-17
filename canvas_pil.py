from __future__ import division

import tkinter as tk
from threading import Thread, Lock, Event

from PIL import Image, ImageTk
from PIL.ImageDraw import ImageDraw

from l_system_utils import PlaceHolder

import tempfile
from os.path import join, isdir, isfile
from os import makedirs

import hashlib

image_cache_dir = join(tempfile.gettempdir(), "lsd_pil_images")

class TurtleCanvas(tk.Canvas):

    def __init__(self, master, *args, **kwargs):

        tk.Canvas.__init__(self, master, *args, **kwargs)
        self._change_state = Lock()
        self._update_image = Event()

        self.c_width = int(self['width'])
        self.c_height = int(self['height'])
        
        self.pil_image = Image.new("RGB", (self.c_width, self.c_height), (255,255,255))
        self.update_this()

    def begin_new(self):
        with self._change_state:
            self.pil_image = Image.new("RGB", (self.c_width, self.c_height), (255,255,255))

    def set_image(self, new_image):
        with self._change_state:
            self.pil_image = new_image

    def update_image(self):
        with self._change_state:
            self._update_image.set()

    def update_this(self):
        if self._update_image.isSet():
            with self._change_state:
                self.photo_image = ImageTk.PhotoImage(self.pil_image)
                self.delete('all')
                self.create_image((self.c_width/2, self.c_height/2), image=self.photo_image)
                self._update_image.clear()
                
        self.update_idletasks()
        self.after(100, self.update_this)
    
class DrawTurtle(Thread):

    def __init__(self, canvas, turtle, colors={}, **kwargs):

        super(DrawTurtle, self).__init__(**kwargs)
        self._stop_drawing = Event()

        self.canvas = canvas
        self.turtle = turtle
        self.colors = colors


    def stop_drawing(self):
        self._stop_drawing.set()
    
    "Draw directly on tkinter canvas"
    def run(self): # no need to overwrite parent's init

        turtle = self.turtle
        colors = self.colors
        
        if self.load_from_cache():
            return

        self.canvas.begin_new()
        im_draw = ImageDraw(self.canvas.pil_image)

        color = self.colors["1"]

        # Calculate size, and scale to fill the frame
        t_width = turtle.rightmost[0] - turtle.leftmost[0]
        t_height = turtle.bottommost[1] - turtle.topmost[1]

        if t_width / t_height > 1: # fat image scale according to width
            scale_factor = self.canvas.c_width / t_width
        else:
            scale_factor = self.canvas.c_height / t_height


        left_margin = (self.canvas.c_width - scale_factor*t_width)  / 2
        top_margin  = (self.canvas.c_height - scale_factor*t_height) / 2

        x_shift = left_margin - scale_factor*turtle.leftmost[0]
        y_shift = top_margin  - scale_factor*turtle.topmost[1]
        
        coordinates = []

        for item in turtle.lines:
            if self._stop_drawing.isSet():
                return
            if isinstance(item, PlaceHolder):
                coordinates.append(item)
            else:
                coordinates.append((item[0]*scale_factor+x_shift,
                                    item[1]*scale_factor+y_shift,
                                    item[2]*scale_factor+x_shift,

                                    item[3]*scale_factor+y_shift))

        i = 0
        for item in coordinates:
            if self._stop_drawing.isSet():
                return

            "Update canvas after each 3000 stroke"
            i += 1
            if i > 3000:
                self.canvas.update_image()
                i = 0
            if isinstance(item, PlaceHolder): # not a list of coordinates
                if item.value in colors:
                    color = colors[item.value]
            else:
                im_draw.line(item, color)

        self.canvas.update_image()

        self.save_to_cache()

    def get_cache_filename(self):
        m = hashlib.sha256()
        m.update(str(self.turtle.angle).encode('utf-8'))
        m.update(";".join("{}:{}".format(x,y) for x,y in self.colors.items()).encode('utf-8'))
        m.update(self.turtle.string.encode('utf-8'))

        return join(image_cache_dir, m.hexdigest() + ".jpg")
        
    def load_from_cache(self):

        filename = self.get_cache_filename()

        if not isfile(filename):
            print("Couldnt find cached image")
            return False

        self.canvas.set_image(Image.open(filename))
        self.canvas.update_image()
        print("Loaded image from cache")
        return True

    
    def save_to_cache(self):
        print("Saving image to cache")

        filename = self.get_cache_filename()

        if not isdir(image_cache_dir):
            makedirs(image_cache_dir)
            
        self.canvas.pil_image.save(filename)


        
