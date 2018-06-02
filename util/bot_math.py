from math import sqrt as math_sqrt

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
        return "Vector2: (%.2f,%.2f)"%(self.x,self.y)
    
    def __repr__(self):
        return "Vector2(%.2f,%.2f)"%(self.x,self.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x*scalar, self.y*scalar)
    
    def __div__(self, scalar):
        return self.__mul__(1.0/scalar)
    
    def __abs__(self):
        return math_sqrt(Vector2.dot(self, self))   
        
    def normalize(self):
        return self/self.__abs__()
    
    @staticmethod 
    def dot(VectorA, VectorB):
        dot = (VectorA.x*VectorB.x) + (VectorA.y*VectorB.y)
        return dot
    
    @staticmethod
    def cross(VectorA, VectorB):
        cross = (VectorA.x*VectorB.y) - (VectorA.y*VectorB.x)
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
    


    
