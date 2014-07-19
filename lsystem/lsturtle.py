from math import sin, cos, radians
from lsystem.l_system_utils import PlaceHolder


class Turtle(object):

    def __init__(self, instructions, angle, placeholders=[], null_characters=[]):
        """
        @param placeholders: they don't change turtle's state, but will be inserted
        into coordinate list as additional information.

        @param null_characters: list of characters that don't do anything.
        These can be useful when generating the string, but they are not directives for turtle
        """
        self.directives = {
            "j": "jump",
            "+": "right",
            "-": "left",
            "U": "up",  # Until pencil is down again, nothing will be drawn
            "D": "down",
            "[": "push",
            "]": "pop",
        }

        self.string = instructions
        self.angle = angle
        self.placeholders = placeholders
        self.null_characters = null_characters
        
        self._pos = (0, 0)
        self._heading = 0

        self.pendown = True

        self._stack = []  # stack of saved position/angles

        # coordinates of border points
        self.leftmost = (0, 0)
        self.rightmost = (0, 0)
        self.topmost = (0, 0)
        self.bottommost = (0, 0)

        """
        _lines: list of tuples of coordinates with placeholders. Looks like,
        [((1,2),(1,3),(2,3)),PlaceHolder("c1"), ((2,4),(3,5))]
        every tuple of coordinates represents a continues line.
        """

        self.lines = []

        self.run()
        
    def run(self):
        for x in self.string:
            try:
                getattr(self, self.directives[x])()
            except KeyError:
                # This character is not a directive. Maybe it is a placeholder, or null character?
                if x in self.null_characters:
                    continue
                elif x in self.placeholders:
                    self.lines.append(PlaceHolder(x))
                else:
                    self.forward()  # Otherwise, we assume this actions is forward
                
    def forward(self):
        x, y = self._pos
        x2, y2 = (x + cos(radians(self._heading)), y + sin(radians(self._heading)))

        self._pos = (x2, y2)

        if x2 < self.leftmost[0]:
            self.leftmost = self._pos

        if x2 > self.rightmost[0]:
            self.rightmost = self._pos

        if y2 < self.topmost[1]:
            self.topmost = self._pos

        if y2 > self.bottommost[1]:
            self.bottommost = self._pos
        
        if self.pendown:
            self.lines.append(tuple((x, y, x2, y2)))

    def right(self):
        self._heading += self.angle

    def left(self):
        self._heading -= self.angle

    def up(self):
        self.pendown = False

    def down(self):
        self.pendown = True

    def jump(self):
        penstate = self.pendown
        self.pendown = False
        self.forward()
        self.pendown = penstate
    
    def push(self):
        self._stack.append((self._pos, self._heading))


    def pop(self):
        self._pos, self._heading = self._stack.pop()
