'''s
Created on May 31, 2018

@author: ashka
'''
from util.bot_math import Vector2
from util.bot_math import Transform

def run():
    a = Vector2(5,5)
    b = Vector2(-5,1)
    
    print (Vector2.dot(a,b))
    print (Vector2.cross(a,b))
    
    print a+b
    print a-b
    print a*2
    print b/2
    
    
    c = Transform(a,50,b)
    
    print c.pos
    
    c.translate(b)
    
    print c.pos
    
    c.rotate(50)
    
    print c.rot
    
    c.scaleBy(b)
    
    print c.scale