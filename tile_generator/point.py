from math import pi, cos, sin, atan2,sqrt
import math

class Point():
    def __init__(self,x, y):
        self.x = x
        self.y = y
    
    def __getitem__(self, index):
        if index == 0: return self.x
        if index == 1: return self.y
        raise IndexError("Point type only supports index 0 and 1")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Point type only supports index 0 and 1")
        return

    def __iter__(self):
        for index in range(2):
            yield self[index]
    
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, other):
        return (other != None) and (abs(self[0] - other[0]) < 10e-10) and (
            abs(self[1] - other[1]) < 10e-10)

    def __ne__(self, other):
        return (other == None) or (abs(self[0] - other[0]) > 10e-10) or (
            abs(self[1] - other[1]) > 10e-10)

    def distance(self, other):
        """  the distance to another coordinate """
        return math.sqrt((other[0] - self.x)**2 + (other[1] - self.y)**2)

    def angle_rad(self, other=(0.0, 0.0)):
        """ the angle with respect to another coordinate, in radians """
        return math.atan2(self.y - other[1], self.x - other[0])

    def __iadd__(self, other):
        self.x += other[0]
        self.y += other[1]
        return self

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])

    def __isub__(self, other):
        self.x -= other[0]
        self.y -= other[1]
        return self

    def __sub__(self, other):
        return Point(self.x - other[0], self.y - other[1])

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)
    
    def __rmul__(self, other):
        return Point(self.x * other, self.y * other)
        
    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __abs__(self):
        return math.sqrt(abs(self.x)**2 + abs(self.y)**2)
