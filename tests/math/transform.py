from util.bot_math import Vector2
from util.bot_math import Transform

def run():
    v = Vector2(5, 5)
    t = Transform()
    t.position += Vector2(15, 10)
    t.rotation += 45
    t.scale = Vector2(2, 2)
    expect = Vector2(15.00, abs(Vector2(10, 10)) + 10)
    result = t.getMatrix() * v
    assert result == expect, "Transform failed: expect %s, got %s."%(expect, result)

    expect = v
    result = t.getMatrix() * t.getInverseMatrix() * v
    assert result == expect, "Transform Inverse failed: expect %s, got %s."%(expect, result)
