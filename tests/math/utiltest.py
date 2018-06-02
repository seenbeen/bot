
from util.bot_math import Vector2
from util.bot_math import Transform

def run():
    a = Vector2(5,5)
    b = Vector2(-5,1)
    print "\nMath Test\n"
    print (Vector2.dot(a,b))
    print "Answer should be: -20\n"
    print (Vector2.cross(a,b))
    print "Answer should be: 30\n"
    
    print a+b 
    print "Answer should be: 0, 6\n"
    print a-b
    print "Answer should be: 10, 4\n"
    print a*2 
    print "Answer should be: -10, 10\n"
    print b/2 
    print "Answer should be: -2.5, 0.5\n"
    
    print abs(a)
    print "Answer should be: 7.1\n"
    
    print a.normalize()
    print "Answer should be: 0.71, 0.71\n"
    
    
    c = Transform(a,50,b)
    
    print c.pos 
    print "Answer should be: 5, 5\n"
    
    c.translate(b)
    
    print c.pos 
    print "Answer should be: 0, 6\n"
    
    c.rotate(50)
    
    print c.rot  
    print "Answer should be: 100\n"
    
    c.scaleBy(b)
    
    print c.scale  
    print "Answer should be: 25, 1\n"