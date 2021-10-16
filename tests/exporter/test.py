from classes.Canvas import Canvas
from classes.Font import Font
from classes.Fill import Fill
from classes.Stroke import Stroke
from classes.primitives.Rect import Rect
from classes.primitives.Circle import Circle
from classes.primitives.Text import Text, Anchor, Baseline
from classes.util.Vector2 import Vector2

"""
|-------|-------|
|       |       |
|   •   |   •   |
|       |       |
|-------|-------|
"""

c = Canvas("test", "svg", Vector2(500, 500), children=[], rotation=0)
rect1 = Rect(True, Vector2(125, 250), 250, 500, stroke=Stroke('black', 5, 1), fill=Fill("white", 1), children=[], rotation=0)
rect2 = Rect(False, Vector2(375, 250), 250, 500, stroke=Stroke('white', 5, 1), fill=Fill("black", 1), children=[], rotation=0)
circle1 = Circle(False, Vector2(0, 0), 50, stroke=None, fill=Fill("black", 1), children=[], rotation=0)
circle2 = Circle(True, Vector2(0, 0), 50, stroke=None, fill=Fill("white", 1), children=[], rotation=0)
text1 = Text("yang", Vector2(0, 0), width = None, halign = Anchor.CENTER, valign = Baseline.CENTER, font=Font("Arial", size=12, weight=400), stroke=None, fill=Fill("white", 1), children=[], rotation=90)
text2 = Text("yin", Vector2(0, 0), width=None, halign = Anchor.CENTER, valign = Baseline.CENTER, font=Font("Arial", size=12, weight=400), stroke=None, fill=Fill("black", 1), children=[], rotation=-90)

c.add_child(rect1)
c.add_child(rect2)
rect1.add_child(circle1)
rect2.add_child(circle2)
circle1.add_child(text1)
circle2.add_child(text2)

print(c.render())
c.export_svg("test.svg")