from ..primitives.Rect import Rect
from ..primitives.Circle import Circle
from ..primitives.Ellipse import Ellipse
from ..primitives.Image import Image
from ..primitives.Line import Line
from ..primitives.Polygon import Polygon
from ..primitives.Text import Text, Anchor, Baseline
from ..util.Vector2 import Vector2

from ..Fill import Fill

import PIL

class Generator:
    def generate_children(self, pw, ph):
        generated = []
        for c in self.children:
            generated.append(c.generate(pw, ph))
        return generated

class RectGenerator(Generator):
    def __init__(self, x, y, width_expr, height_expr, fill=None, stroke=None, rotate=0, clipped=False, children=[]):
        self.x, self.y = x, y
        self.width_expr = width_expr
        self.height_expr = height_expr
        self.fill = fill
        self.stroke = stroke
        self.rotate = rotate
        self.clipped = clipped
        self.children = children

    def generate(self, pw, ph):
        width = self.width_expr.eval(pw, ph)
        height = self.height_expr.eval(pw, ph)
        pos = Vector2(self.x.eval(pw, ph), self.y.eval(pw, ph))
        children = self.generate_children(width, height)
        return Rect(self.clipped, pos, width, height, self.stroke, self.fill, children, self.rotate)

class CircleGenerator(Generator):
    def __init__(self, x, y, radius_expr, fill=None, stroke=None, rotate=0, clipped=False, children=[]):
        self.x, self.y = x, y
        self.radious_expr = radious_expr
        self.fill = fill
        self.stroke = stroke
        self.rotate = rotate
        self.clipped = clipped
        self.children = children

    def generate(self, pw, ph):
        radius = self.radius_expr.eval(pw, ph)
        pos = Vector2(self.x.eval(pw, ph), self.y.eval(pw, ph))
        children = self.generate_children(radius*2, radius*2)
        return Circle(self.clipped, pos, radius, self.stroke, self.fill, children, self.rotate)

class EllipseGenerator(Generator):
    def __init__(self, x, y, xrad_expr, yrad_expr, fill=None, stroke=None, rotate=0, clipped=False, children=[]):
        self.x, self.y = x, y
        self.xrad_expr = xrad_expr
        self.yrad_expr = yrad_expr
        self.fill = fill
        self.stroke = stroke
        self.rotate = rotate
        self.clipped = clipped
        self.children = children

    def generate(self, pw, ph):
        xrad = self.xrad_expr.eval(pw, ph)
        yrad = self.yrad_expr.eval(pw, ph)
        pos = Vector2(self.x.eval(pw, ph), self.y.eval(pw, ph))
        children = self.generate_children(xrad*2, yrad*2)
        return Ellipse(self.clipped, pos, xrad, yrad, self.stroke, self.fill, children, self.rotate)

class LineGenerator(Generator):
    def __init__(self, x1, y1, x2, y2, stroke=None):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.stroke = stroke

    def generate(self, pw, ph):
        pos1 = Vector2(self.x1.eval(pw, ph), self.y1.eval(pw, ph))
        pos2 = Vector2(self.x2.eval(pw, ph), self.y2.eval(pw, ph))
        return Line(False, pos1, pos2, self.stroke, [], 0)
        
class PolygonGenerator(Generator):
    def __init__(self, points, fill=None, stroke=None, rotate=0, clipped=False, children=[]):
        self.points = points
        self.fill = fill
        self.stroke = stroke
        self.rotate = rotate
        self.clipped = clipped
        self.children = children

    def generate(self, pw, ph):
        points = [Vector2(P[0].eval(pw, ph), P[1].eval(pw, ph)) for P in self.points]
        xs = [p.x for p in points]
        ys = [p.y for p in points]
        children = self.generate_children(abs(min(xs)-max(xs)), abs(min(ys), max(ys)))
        return Polygon(self.clipped, points, self.stroke, self.fill, children, self.rotate)

class ImageGenerator(Generator):
    def __init__(self, x, y, width_expr, height_expr=None, path="", rotate=0):
        self.x, self.y = x, y
        self.width_expr = width_expr
        self.height_expr = height_expr
        self.path = path
        self.rotate = rotate

    def generate(self, pw, ph):
        width = self.width_expr.eval(pw, ph)
        height = 0
        img = PIL.Image.open(self.path) # For image auto scaling
        iw, ih = img.size
        if height_expr != None:
            height = self.height_expr.eval(pw, ph)
        else:
            height = width * (ih / iw)
        size = Vector2(width, height)
        pos = Vector2(self.x.eval(pw, ph), self.y.eval(pw, ph))
        return Image(self.path, pos, size, [], self.rotate)

class TextGenerator(Generator):
    def __init__(self, x, y, text, font, color, align="center", width_expr=None, rotate=0):
        self.x, self.y = x, y
        self.text = text
        self.font = font
        self.color = color
        self.align = align
        self.width_expr = width_expr
        self.rotate = rotate

    def generate(self, pw, ph):
        width = None
        if self.width_expr != None:
            width = self.width_expr.eval(pw, ph)
        
        align = Anchor.CENTER
        if self.align == "left":
            align = Anchor.LEFT
        elif self.align == "right":
            align = Anchor.RIGHT

        pos = Vector2(self.x.eval(pw, ph), self.y.eval(pw, ph))
        return Text(self.text, pos, width, align, Baseline.TOP, self.font, None, Fill(self.color, 1), [], self.rotate)