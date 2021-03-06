from util.bot_math import Vector2
from util.bot_math import Transform

def run():
    a = Vector2(3,4)
    b = Vector2(-5,12)
    
    assert Vector2.dot(a,b) == 33, "dot test. Answer should be: 33\n"
    
    assert (Vector2.cross(a,b)) == 56, "cross test. Answer should be: 56\n"
    
    assert (a+b) == Vector2(-2,16), "add test. Answer should be: -2, 16\n"
    
    assert a-b == Vector2(8,-8), "sub test. Answer should be: 8, -8\n"
    assert a*2 == Vector2(6,8), "mul test. Answer should be: 6, 8\n"
    
    assert b/2 == Vector2(-2.5, 6), "div test. Answer should be: -2.5, 6\n"
    assert abs(a) == 5, "abs test. Answer should be: 5\n"
    
    assert a.normalize() == Vector2(3.0/5, 4.0/5), "normalize test. Answer should be: 3/5, 4/5\n"
