from operator import pos
from cmath import sqrt


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, vector):
        x = self.x + vector.x
        y = self.y + vector.y
        return Vector2(x,y)
        
    def __sub__(self, vector):
        x = self.x - vector.x
        y = self.y - vector.y
        return Vector2(x,y)
    
    def __str__(self):
        return "(%i,%i)"%(self.x,self.y)
    
    def __repr__(self):
        return "(%i,%i)"%(self.x,self.y)
    
    def __mul__(self, other):
        x = self.x*other
        y = self.y*other
        return Vector2(x,y)
    
    def __div__(self, other):
        x = self.x/other
        y = self.y/other
        return Vector2(x,y)
    
    def magnitude(self):
        return sqrt(self.x * self.x + self.y * self.y)   
        
    def normalized(self):
        l = self.magnitude()
        
        x = self.x / l
        y = self.y / l
        
        return Vector2(x,y)
    
    @staticmethod 
    def dot(VectorA, VectorB):
        A = VectorA.normalized()
        B = VectorB.normalized()
        dot = (A.x*B.x) + (A.y*B.y)
        return dot
    
    @staticmethod
    def cross(VectorA, VectorB):
        A = VectorA.normalized()
        B = VectorB.normalized()
        cross = (A.x*B.y) - (A.y*B.x)
        return cross
    
class Transform:
    def __init__(self, position, rot, scale):
        self.pos = position
        self.rot = rot
        self.scale = scale
        
    def rotate(self, degrees):
        self.rot += degrees

    def translate(self, vector):
        self.pos = self.pos + vector
    
    def scaleBy(self, scaleVector):
        self.scale.x = self.scale.x * scaleVector.x
        self.scale.y = self.scale.y * scaleVector.y
    


    
