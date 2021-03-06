from math import sqrt as math_sqrt
from math import cos as math_cos
from math import sin as math_sin
from math import radians as math_radians
from math import degrees as math_degrees
from math import atan2 as math_atan2
import pygame

def sign(x):
    return [1, -1][x < 0]

class Vector2:
    # Notes: we really should start doing type checks for everything here,
    # but that /does/ also introduce some efficiency cuts

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, vector):
        return Vector2(self.x + vector.x, self.y + vector.y)

    def __iadd__(self, vector):
        return self + vector

    def __sub__(self, vector):
        return Vector2(self.x - vector.x, self.y - vector.y)

    def __isub__(self, vector):
        return self - vector
    
    def __mul__(self, primitive):
        if isinstance(primitive, float) or isinstance(primitive, int):
            return Vector2(self.x * primitive, self.y * primitive)
        elif isinstance(primitive, Vector2):
            return Vector2(self.x * primitive.x, self.y * primitive.y)
        else:
            raise Exception("Unknown operand type passed to Vector2 mul.")

    def __imul__(self, primitive):
        return self * primitive

    def __div__(self, primitive):
        if isinstance(primitive, float) or isinstance(primitive, int):
            return self * (1.0/primitive)
        elif isinstance(primitive, Vector2):
            return Vector2(self.x / primitive.x, self.y / primitive.y)
        else:
            raise Exception("Unknown operand type passed to Vector2 div.")

    def __idiv__(self, primitive):
        return self / primitive

    def __neg__(self):
        return self * (-1)

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

    def toIntTuple(self):
        return map(int, (self.x, self.y))

    def __str__(self):
        return "Vector2: (%.2f, %.2f)"%(self.x, self.y)
    
    def __repr__(self):
        return "Vector2(%f, %f)"%(self.x, self.y)
        
    def copy(self):
        return Vector2(self.x, self.y)
    
    def copyTo(self, vec):
        vec.x = self.x
        vec.y = self.y

# This is an incomplete Mat33 class, good enough to
# support basic transforms for now
class Mat33:
    __MAT_IDENTITY = [[1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]]
    def __init__(self, mat=__MAT_IDENTITY):
        self.mat = map(lambda x: map(float, x), mat)

    def setElem(self, r, c, v):
        self.mat[r][c] = v

    def getElem(self, r, c):
        return self.mat[r][c]

    # very crappy way to multiply.  oh well
    def __mul__(self, primitive):
        if isinstance(primitive, Mat33):
            transposedData = zip(*primitive.mat)
            result = Mat33()
            for i in range(3):
                for j in range(3):
                    result.setElem(i, j,
                                   reduce(lambda x,y: x + y,
                                          map(lambda x,y: x * y, self.mat[i], transposedData[j])))
            return result

        elif isinstance(primitive, Vector2):
            data = [primitive.x, primitive.y, 1.0]
            result = []
            for i in range(3):
                result.append(reduce(lambda x,y: x + y,
                                     map(lambda x,y: x * y, self.mat[i], data)))
            return Vector2(result[0], result[1])

        else:
            raise Exception("Unrecognized operand for Mat33 mul")

    def __repr__(self):
        return "Mat33(["+", ".join(map(lambda x: "[" + ", ".join(map(str, x)) + "]", self.mat)) + "])"

    def __str__(self):
        return "Matrix(["+",\n\t".join(map(lambda x: "[" + ", ".join(map(str, x)) + "]", self.mat)) + "])"

class Mat33Util:
    @staticmethod
    def getRotationMatrix(angle):
        radiansAngle = math_radians(angle)
        # 9 digits of precision should be more than enough
        sinAngle = round(math_sin(radiansAngle),9)
        cosAngle = round(math_cos(radiansAngle),9)
        return Mat33([[cosAngle, -sinAngle, 0],
                      [sinAngle, cosAngle, 0],
                      [0, 0, 1]])
    @staticmethod
    def getTranslationMatrix(dx, dy):
        result = Mat33()
        result.setElem(0, 2, dx)
        result.setElem(1, 2, dy)
        return result

    @staticmethod
    def getScaleMatrix(sx, sy):
        result = Mat33()
        result.setElem(0, 0, sx)
        result.setElem(1, 1, sy)
        return result

    @staticmethod
    def getCamMatrix(camTransform, camDims):
        return (Mat33Util.getScaleMatrix(1.0 / camDims.x, 1.0 / camDims.y) *
                camTransform.getInverseMatrix())

    @staticmethod
    def getViewportMatrix(vpPosition, vpDims):
        '''vpDims [Vector2], vpPosition [Vector2] - in ScreenSpace coordinates''' 
        return (Mat33Util.getTranslationMatrix(vpPosition.x, vpDims.y + vpPosition.y) *
                Mat33Util.getScaleMatrix(vpDims.x, -vpDims.y) *
                Mat33Util.getTranslationMatrix(0.5, 0.5))

class Transform:
    '''
        Transformations are applied as follows:
        1. Scaling
        2. Rotation
        3. Translation
    '''
    def __init__(self):
        self.position = Vector2()
        self.rotation = 0.0
        self.scale = Vector2(1, 1)

    def getMatrix(self):
        # TODO: Maybe cache matrices to save some construction
        return (Mat33Util.getTranslationMatrix(self.position.x, self.position.y) *
                Mat33Util.getRotationMatrix(self.rotation) *
                Mat33Util.getScaleMatrix(self.scale.x, self.scale.y))
    def getInverseMatrix(self):
        return (Mat33Util.getScaleMatrix(1.0 / self.scale.x, 1.0 / self.scale.y) *
                Mat33Util.getRotationMatrix(-self.rotation) *
                Mat33Util.getTranslationMatrix(-self.position.x, -self.position.y))
        
    def copy(self):
        temp = Transform()
        self.copyTo(temp)
        return temp
    
    def copyTo(self, xform):
        self.position.copyTo(xform.position)
        xform.rotation = self.rotation
        self.scale.copyTo(xform.scale)

    '''
        By no means efficient, and should probably be used sparingly, attempts to decompose
        a given matrix into its transformation consistuents.
        Note that since multiple linear combinations exist for any given
        transformation matrix, this function can't really be used to generate
        a comparable transform.
    '''
    @staticmethod
    def fromMat33(mat):
        p1, p2, p3 = map(lambda p: Vector2(*p), [(0, 0), (1, 0), (0, 1)])
        tp1, tp2, tp3 = map(lambda v: mat * v, [p1, p2, p3])

        t = Transform()

        # extract translation
        t.position = tp1
        # extract rotation
        angleVec = tp2 - tp1
        t.rotation = math_degrees(math_atan2(angleVec.y, angleVec.x))
        # extract scale
        t.scale = Vector2(abs(tp2 - tp1) / abs(p2 - p1),
                          abs(tp3 - tp1) / abs(p3 - p1))
        t.scale.y *= sign(Vector2.cross(tp3 - tp1, tp2 - tp1))
        return t

class RectUtil:
    @staticmethod
    def findAABB(pts):
        if len(pts) == 0:
            raise Exception("Please provide at least one point to method findAABB")

        minX, minY = pts[0].x, pts[0].y
        maxX, maxY = pts[0].x, pts[0].y
        
        for p in pts:
            minX = min(minX, p.x)
            minY = min(minY, p.y)
            maxX = max(maxX, p.x)
            maxY = max(maxY, p.y)

        return pygame.Rect(map(int, [minX, minY, maxX - minX, maxY - minY]))

    @staticmethod
    def genRectPts(rect):
        p = Vector2(rect.x, rect.y)
        w = Vector2(rect.w, 0)
        h = Vector2(0, rect.h)
        return [p, p+w, p+w+h, p+h]
