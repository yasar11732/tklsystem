from __future__ import division

from threading import Thread, Event
from queue import Queue, Empty

import tkinter as tk
from lsystem.l_system_utils import PlaceHolder
    

class TurtleCanvas(tk.Canvas):

    def __init__(self, master, *args, **kwargs):

        tk.Canvas.__init__(self, master, *args, **kwargs)
        self.pil_image = None
        self._q = Queue()
        self._cancel_current = Event()
        self.update_this()

    def begin_new(self):
        self._q = Queue()
        self._q.put((None, None))

    def queue_line(self, line, color):
        self._q.put((line, color))

    def update_this(self):
        try:
            for i in range(4000):  # draw 2000 lines at a cycle
                line, color = self._q.get_nowait()
                if line is None:
                    self.delete('all')
                    continue
                self.create_line(*line, fill=color)

        except Empty:
            pass
        
        self.update_idletasks()
        self.after(5, self.update_this)
            

class DrawTurtle(Thread):

    def __init__(self, canvas, turtle, colors={}, **kwargs):

        super(DrawTurtle, self).__init__(**kwargs)
        self._stop_drawing = Event()

        self.canvas = canvas
        self.turtle = turtle
        self.colors = colors

    def stop_drawing(self):
        self._stop_drawing.set()
        
    def run(self):

        self.canvas.begin_new()
        color = self.colors["1"]

        # Calculate size, and scale to fill the frame
        t_width = self.turtle.rightmost[0] - self.turtle.leftmost[0]
        t_height = self.turtle.bottommost[1] - self.turtle.topmost[1]

        c_width = int(self.canvas['width'])
        c_height = int(self.canvas['height'])

        if t_width / t_height > 1:  # fat image scale according to width
            scale_factor = c_width / t_width
        else:
            scale_factor = c_height / t_height

        left_margin = (c_width - scale_factor*t_width) / 2
        top_margin = (c_height - scale_factor*t_height) / 2

        x_shift = left_margin - scale_factor*self.turtle.leftmost[0]
        y_shift = top_margin - scale_factor*self.turtle.topmost[1]
        
        coordinates = []

        for item in self.turtle.lines:
            if self._stop_drawing.isSet():
                return
            if isinstance(item, PlaceHolder):
                coordinates.append(item)
            else:
                coordinates.append((item[0]*scale_factor+x_shift,
                                    item[1]*scale_factor+y_shift,
                                    item[2]*scale_factor+x_shift,
                                    item[3]*scale_factor+y_shift))
            
        for item in coordinates:
            if self._stop_drawing.isSet():
                return
            if isinstance(item, PlaceHolder):  # not a list of coordinates
                if item.value in self.colors:
                    color = self.colors[item.value]
            else:
                self.canvas.queue_line(item, color)
