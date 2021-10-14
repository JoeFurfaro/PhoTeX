from classes.Canvas import Canvas
from classes.Fill import Fill
from classes.Stroke import Stroke
from classes.primitives.Rect import Rect
from classes.util.Vector2 import Vector2


c = Canvas([], "test", "svg", Vector2(500, 500), rotation=0)
r1 = Rect([], False, Vector2(150, 225), 200, 50, stroke=None, fill=Fill("red", 0.1), rotation=0)
r2 = Rect([], False, Vector2(150, 225), 200, 50, stroke=None, fill=Fill("blue", 0.3), rotation=0)

c.add_child(r1)
r1.add_child(r2)

print(c.render())
print(r1.parent)
print(r1.depth)
print(r2.depth)
