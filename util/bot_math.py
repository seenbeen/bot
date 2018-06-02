from math import sqrt as math_sqrt

class Vector2:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, vector):
        return Vector2(self.x + vector.x, self.y + vector.y)
        
    def __sub__(self, vector):
        return Vector2(self.x - vector.x, self.y - vector.y)
    
    def __str__(self):
        return "Vector2: (%.2f, %.2f)"%(self.x, self.y)
    
    def __repr__(self):
        return "Vector2(%f, %f)"%(self.x, self.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __div__(self, scalar):
        return self * (1.0/scalar)
    
    def __abs__(self):
        return math_sqrt(Vector2.dot(self, self))
    
    def __eq__(self, vector):
        epsilon = 0.000001
        return (abs(self.x - vector.x) <= epsilon and abs(self.y - vector.y) <= epsilon)
        
    def normalize(self):
        return self / abs(self)
    
    @staticmethod 
    def dot(VectorA, VectorB):
        return (VectorA.x * VectorB.x) + (VectorA.y * VectorB.y)
    
    @staticmethod
    def cross(VectorA, VectorB):
        return (VectorA.x * VectorB.y) - (VectorA.y * VectorB.x)
    
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
    


    
