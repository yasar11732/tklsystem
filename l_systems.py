from PIL import Image, ImageTk
from PIL.ImageDraw import ImageDraw
from math import sin, cos, radians

import tkinter as tk

class LindenmayerException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class Lindenmayer(ImageDraw):

    syms = {
        "j":"jump",
        "+":"right",
        "-":"left",
        "U":"up", # Untl pencil is down again, nothing will be drawn
        "D":"down",
        "[":"push",
        "]":"pop",
        "1":"c1",
        "2":"c2", 
        "3":"c3", 
        "4":"c4", 
    }

    control_strings = ("LB", "COLOR")

    def init(self, iterations, angle, axiom, rules,
             constants="",
             color1 = "#000000",
             color2 = "#dd0000",
             color3 = "#00dd00",
             color4 = "#0000dd"):

        self.pos = (0,0)
        self.heading = 0
        
        self.iterations = iterations
        self.angle = angle
        self.constants = constants
        self.axiom = axiom
        self.rules = rules

        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.color4 = color4

        self.pendown = True

        self._stack = []
        self._coordinate_list = [self.pos]

        self._all_points = []

        self.add_unit_rules()
        self.create_string()

        self.execute()

    def add_unit_rules(self):

        "Elements with no rules will stay the same"
        units = self.axiom + "".join(self.rules.keys()) + "".join(self.rules.values())

        for x in set(units):

            if not x in self.rules.keys():
                self.rules[x] = x

    def create_string(self):
        
        string = self.axiom
        
        for _ in range(self.iterations):
            string = "".join(self.rules[x] for x in string)

        self.string = string

    def shift_coordinates(self, byx, byy):

        temp = []
        for x,y in self._coordinate_list:
            if x in self.control_strings:
                temp.append((x,y))
            else:
                temp.append((x+byx, y+byy))

        self._coordinate_list = temp

    def scale_coordinates(self, byx, byy):

        temp = []
        for x,y in self._coordinate_list:
            if x in self.control_strings:
                temp.append((x,y))
            else:
                temp.append((x*byx, y*byy))

        self._coordinate_list = temp
        

    def execute(self):
        self._coordinate_list = [("COLOR",self.color1)]

        # 1) Calculate coordinates
        for x in self.string:
            try:
                getattr(self,self.syms[x])()
            except KeyError as err:
                if x in self.constants: # This is a dummy action
                    continue
                else:
                    self.forward()

        
        # 2) Resize the coordinates to fit into image
        minx, miny, maxx, maxy = 0, 0, 0, 0

        for x,y in self._coordinate_list:
            if x in self.control_strings:
                continue
            if x < minx:
                minx = x
            if y < miny:
                miny = y
            if x > maxx:
                maxx = x
            if y > maxy:
                maxy = y
        self.shift_coordinates(-1 * minx, -1 * miny)

        cw, ch = maxx-minx, maxy-miny

        if ch / cw > 1: # tall image
            scale_factor = self.im.size[1] / ch
        else:
            scale_factor = self.im.size[0] / cw

        self.scale_coordinates(scale_factor, scale_factor)

        self.finalize()

    def finalize(self):

        temp = []
        for x,y in self._coordinate_list:
            if x not in self.control_strings:
                temp.append((x,y))
            else:
                if x == "LB": # line break
                    self.line(temp, self.color)
                    temp = []
                if x == "COLOR": # change color
                    self.color = y

        if len(temp) > 1:
            self.line(temp, self.color)

    def forward(self):

        x, y = self.pos
        self.pos = (x + cos(radians(self.heading)), y + sin(radians(self.heading)))
        if self.pendown:
            self._coordinate_list.append(self.pos)

    def right(self): self.heading += self.angle
    def left(self):  self.heading -= self.angle
    def up(self):    self.pendown = False
    def down(self):  self.pendown = True

    def c1(self): self._coordinate_list.append(("COLOR",self.color1))
    def c2(self): self._coordinate_list.append(("COLOR",self.color2))
    def c3(self): self._coordinate_list.append(("COLOR",self.color3))
    def c4(self): self._coordinate_list.append(("COLOR",self.color4))
    
    def push(self): self._stack.append((self.pos, self.heading))


    def pop(self):
        self.pos, self.heading = self._stack.pop()
        self._coordinate_list += [("LB",""), self.pos]
    

        
        
        
