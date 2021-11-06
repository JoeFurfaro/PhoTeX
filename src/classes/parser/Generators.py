from os import stat
from ..primitives.Rect import Rect
from ..primitives.Circle import Circle
from ..primitives.Ellipse import Ellipse
from ..primitives.Image import Image
from ..primitives.Line import Line
from ..primitives.Polygon import Polygon
from ..primitives.Text import Text, Anchor, Baseline
from ..util.Vector2 import Vector2

from ..Fill import Fill
from ..Stroke import Stroke
from ..Clip import Clip

from ..parser.Expressions import *

from lark import Tree, Token

from .Constants import *

import PIL
import sys

class Generator:
    def generate_children(self, pw, ph):
        generated = []
        for c in self.children:
            generated.append(c.generate(pw, ph))
        return generated

    # Override this for each generator!
    @staticmethod
    def from_parse_tree(self):
        return None

    @staticmethod
    def from_item_list(item_list_tree, defs): # Returns a list of generators from an item_list in parse tree
        generators = []
        item_list = [i.children[0] for i in item_list_tree]
        for item in item_list:
            T = item.data
            if T == ATTRIBS.RECT.value:
                generators.append(RectGenerator.from_parse_tree(item, defs))
            elif T == ATTRIBS.CIRCLE.value:
                generators.append(CircleGenerator.from_parse_tree(item, defs))
            elif T == ATTRIBS.ELLIPSE.value:
                generators.append(EllipseGenerator.from_parse_tree(item, defs))
            elif T == ATTRIBS.LINE.value:
                generators.append(LineGenerator.from_parse_tree(item, defs))
            elif T == ATTRIBS.POLYGON.value:
                generators.append(PolygonGenerator.from_parse_tree(item, defs))
            elif T == ATTRIBS.IMAGE.value:
                generators.append(ImageGenerator.from_parse_tree(item, defs))
            elif T == ATTRIBS.TEXT.value:
                generators.append(TextGenerator.from_parse_tree(item, defs))
            elif T == ATTRIBS.CUSTOM.value:
                # Lookup for custom type identifier
                ID_tree = Generator.find_in_tree(item, ATTRIBS.IDENTIFIER.value)
                ID = ID_tree[0]
                if not defs.has_type(ID.value):
                    Generator.exception(ID.line, ID.column, "Custom type with identifier '" + ID.value + "' has not been declared")
                type_def = defs.get_type(ID.value)
                x = expression_from_tree(Generator.find_in_tree(item, ATTRIBS.POSITION.value)[0])
                y = expression_from_tree(Generator.find_in_tree(item, ATTRIBS.POSITION.value)[1])

                width = None
                height = None

                if type_def.has_preset_size():
                    width = type_def.width
                    height = type_def.height
                else:
                    width_tree = Generator.find_in_tree(item, ATTRIBS.SIZE.value)
                    if width_tree != None:
                        width = expression_from_tree(Generator.find_in_tree(item, ATTRIBS.SIZE.value)[0])
                        height = expression_from_tree(Generator.find_in_tree(item, ATTRIBS.SIZE.value)[1])

                if width == None or height == None:
                    Generator.exception(ID.line, ID.column, "Variable-sized custom type declaration must include width and height")
                
                generators.append(type_def.construct_generator(x, y, width, height))
        return generators

    @staticmethod
    def find_in_tree(tree, key):
        for x in tree.children:
            if x.data == key:
                return x.children
        return None

    @staticmethod 
    def children_from_tree(tree, defs):
        data = [x.data for x in tree.children]
        children = []
        if ATTRIBS.ITEM_LIST.value in data:
            item_list = Generator.find_in_tree(tree, ATTRIBS.ITEM_LIST.value)
            children = Generator.from_item_list(item_list, defs)
        return children
        
    @staticmethod
    def fill_from_tree(tree, defs):
        data = [x.data for x in tree.children]
        if ATTRIBS.COLOR.value in data:
            c_tree = Generator.find_in_tree(tree, ATTRIBS.COLOR.value)
            fill_color = None
            color_type = c_tree[0].data
            c_token = c_tree[0].children[0]
            if color_type == ATTRIBS.IDENTIFIER.value:
                cID = c_token.value
                fill_color = defs.get_color(cID)
                if fill_color == None:
                    Generator.exception(c_token.line, c_token.column, "Unrecognized color identifier '" + cID + "' in fill color")
            elif color_type == ATTRIBS.HEX_COLOR.value:
                fill_color = str(c_token.value)
            return Fill(fill_color, 1.0)
        return None

    @staticmethod
    def color_from_tree(tree, defs):
        data = [x.data for x in tree.children]
        if ATTRIBS.COLOR.value in data:
            c_tree = Generator.find_in_tree(tree, ATTRIBS.COLOR.value)
            color_type = c_tree[0].data
            c_token = c_tree[0].children[0]
            if color_type == ATTRIBS.IDENTIFIER.value:
                cID = c_token.value
                color = defs.get_color(cID)
                if color == None:
                    Generator.exception(c_token.line, c_token.column, "Unrecognized color identifier '" + cID + "' in text color")
                return color
            elif color_type == ATTRIBS.HEX_COLOR.value:
                return str(c_token.value)
        return None

    @staticmethod
    def font_from_tree(tree, defs):
        data = [x.data for x in tree.children]
        if ATTRIBS.FONT.value in data:
            f_tree = Generator.find_in_tree(tree, ATTRIBS.FONT.value)
            fID = f_tree[0].value
            font = defs.get_font(fID)
            if font == None:
                Generator.exception(f_tree[0].line, f_tree[0].column, "Unrecognized font identifier '" + fID + "' in text definition")
            return font.obj
        return None

    @staticmethod
    def rotate_from_tree_modifier(tree, defs):
        for modifier in tree.children[0].children:
            M = modifier.children[0]
            Mname = M.data if type(M) == Tree else M.value
            if type(M) == Tree:
                if Mname == ATTRIBS.ROTATED.value:
                    return int(M.children[0].children[0].value)
        return 0

    @staticmethod
    def clip_from_tree_modifier(tree, defs):
        for modifier in tree.children[0].children:
            M = modifier.children[0]
            Mname = M.data if type(M) == Tree else M.value
            if type(M) == Tree:
                if Mname == ATTRIBS.CLIPPED.value:
                    if len(M.children) > 0 and M.children[0].children[0].value == CLIP_TYPE.OUT.value:
                        return Clip(False)
                    else:
                        return Clip(True)
        return None

    @staticmethod
    def outline_from_tree_modifier(tree, defs):
        for modifier in tree.children[0].children:
            M = modifier.children[0]
            Mname = M.data if type(M) == Tree else M.value
            if type(M) == Tree:
                if Mname == ATTRIBS.OUTLINED.value:
                    color_type = M.children[0].children[0].data
                    stroke_color = None
                    c_token = M.children[0].children[0].children[0]
                    if color_type == ATTRIBS.IDENTIFIER.value:
                        cID = c_token
                        stroke_color = defs.get_color(cID)
                        if stroke_color == None:
                            Generator.exception(c_token.line, c_token.column, "Unrecognized color identifier '" + cID + "' in outline color")
                    elif color_type == ATTRIBS.HEX_COLOR.value:
                        stroke_color = str(c_token.value)
                    thickness = int(M.children[1].children[0].value)
                    return Stroke(stroke_color, thickness, opacity=1)
        return None

    @staticmethod
    def stroke_from_tree(tree, defs):
        data = [x.data for x in tree.children]
        thickness = 1
        color = DEFAULTS.FILL_COLOR
        if ATTRIBS.THICKNESS.value in data:
            thick_tree = Generator.find_in_tree(tree, ATTRIBS.THICKNESS.value)
            thickness = int(thick_tree[0].value)
        if ATTRIBS.COLOR.value in data:
            color_tree = Generator.find_in_tree(tree, ATTRIBS.COLOR.value)[0]
            c_token = color_tree.children[0]
            if color_tree.data == ATTRIBS.IDENTIFIER.value:
                color = defs.get_color(c_token.value)
                if color == None:
                    Generator.exception(c_token.line, c_token.column, "Unrecognized color identifier '" + c_token.value + "' in outline color")
            elif color_tree.data == ATTRIBS.HEX_COLOR.value:
                color = str(c_token.value)
        return Stroke(color, thickness, 1.0)

    @staticmethod
    def align_from_tree_modifier(tree, defs):
        for modifier in tree.children[0].children:
            M = modifier.children[0]
            Mname = M.data if type(M) == Tree else M.value
            if type(M) == Token:
                if Mname == STATIC_MODIFIER.LEFT:
                    return STATIC_MODIFIER.LEFT
                elif Mname == STATIC_MODIFIER.RIGHT:
                    return STATIC_MODIFIER.RIGHT
        return STATIC_MODIFIER.CENTER

    @staticmethod
    def validate_modifiers(tree, allowed_modifiers):
        for modifier in tree.children[0].children:
            M = modifier.children[0]
            Mname = M.data if type(M) == Tree else M.value
            if Mname not in allowed_modifiers:
                Generator.exception(M.line, M.column, "Illegal modifier '" + Mname + "' supplied in definition")

    @staticmethod
    def exception(line, col, msg):
        print("Exception on line " + str(line) + " column " + str(col) + ": " + str(msg))
        sys.exit(1)
        

class RectGenerator(Generator):
    def __init__(self, x, y, width_expr, height_expr, fill=None, stroke=None, rotate=0, clip=None, children=[]):
        self.x, self.y = x, y
        self.width_expr = width_expr
        self.height_expr = height_expr
        self.fill = fill
        self.stroke = stroke
        self.rotate = rotate
        self.clip = clip
        self.children = children

    def generate(self, pw, ph):
        width = self.width_expr.eval(pw, ph)
        height = self.height_expr.eval(pw, ph)
        pos = Vector2(self.x.eval(pw, ph), self.y.eval(pw, ph))
        children = self.generate_children(width, height)
        return Rect(self.clip, pos, width, height, self.stroke, self.fill, children, self.rotate)

    @staticmethod
    def from_parse_tree(tree, defs):
        pos = Generator.find_in_tree(tree, ATTRIBS.POSITION.value)
        size = Generator.find_in_tree(tree, ATTRIBS.SIZE.value)
        x = expression_from_tree(pos[0])
        y = expression_from_tree(pos[1])
        width = expression_from_tree(size[0])
        height = expression_from_tree(size[1])

        children = Generator.children_from_tree(tree, defs)
        fill = Generator.fill_from_tree(tree, defs)

        Generator.validate_modifiers(tree, (ATTRIBS.ROTATED.value, ATTRIBS.CLIPPED.value, ATTRIBS.OUTLINED.value))
        
        rotate = Generator.rotate_from_tree_modifier(tree, defs)
        clip = Generator.clip_from_tree_modifier(tree, defs)
        stroke = Generator.outline_from_tree_modifier(tree, defs)

        return RectGenerator(x, y, width, height, fill, stroke, rotate, clip, children)


class CircleGenerator(Generator):
    def __init__(self, x, y, radius_expr, fill=None, stroke=None, rotate=0, clip=None, children=[]):
        self.x, self.y = x, y
        self.radius_expr = radius_expr
        self.fill = fill
        self.stroke = stroke
        self.rotate = rotate
        self.clip = clip
        self.children = children

    def generate(self, pw, ph):
        radius = self.radius_expr.eval(pw, ph)
        pos = Vector2(self.x.eval(pw, ph), self.y.eval(pw, ph))
        children = self.generate_children(radius*2, radius*2)
        return Circle(self.clip, pos, radius, self.stroke, self.fill, children, self.rotate)

    @staticmethod
    def from_parse_tree(tree, defs):
        pos = Generator.find_in_tree(tree, ATTRIBS.POSITION.value)
        x = expression_from_tree(pos[0])
        y = expression_from_tree(pos[1])
        rad = expression_from_tree(tree.children[2])

        children = Generator.children_from_tree(tree, defs)
        fill = Generator.fill_from_tree(tree, defs)

        Generator.validate_modifiers(tree, (ATTRIBS.ROTATED.value, ATTRIBS.CLIPPED.value, ATTRIBS.OUTLINED.value))
        
        rotate = Generator.rotate_from_tree_modifier(tree, defs)
        clip = Generator.clip_from_tree_modifier(tree, defs)
        stroke = Generator.outline_from_tree_modifier(tree, defs)

        return CircleGenerator(x, y, rad, fill, stroke, rotate, clip, children)

class EllipseGenerator(Generator):
    def __init__(self, x, y, xrad_expr, yrad_expr, fill=None, stroke=None, rotate=0, clip=None, children=[]):
        self.x, self.y = x, y
        self.xrad_expr = xrad_expr
        self.yrad_expr = yrad_expr
        self.fill = fill
        self.stroke = stroke
        self.rotate = rotate
        self.clip = clip
        self.children = children

    def generate(self, pw, ph):
        xrad = self.xrad_expr.eval(pw, ph)
        yrad = self.yrad_expr.eval(pw, ph)
        pos = Vector2(self.x.eval(pw, ph), self.y.eval(pw, ph))
        children = self.generate_children(xrad*2, yrad*2)
        return Ellipse(self.clip, pos, xrad, yrad, self.stroke, self.fill, children, self.rotate)
    
    @staticmethod
    def from_parse_tree(tree, defs):
        pos = Generator.find_in_tree(tree, ATTRIBS.POSITION.value)
        x = expression_from_tree(pos[0])
        y = expression_from_tree(pos[1])
        xrad = expression_from_tree(tree.children[2])
        yrad = expression_from_tree(tree.children[3])

        children = Generator.children_from_tree(tree, defs)
        fill = Generator.fill_from_tree(tree, defs)

        Generator.validate_modifiers(tree, (ATTRIBS.ROTATED.value, ATTRIBS.CLIPPED.value, ATTRIBS.OUTLINED.value))
        
        rotate = Generator.rotate_from_tree_modifier(tree, defs)
        clip = Generator.clip_from_tree_modifier(tree, defs)
        stroke = Generator.outline_from_tree_modifier(tree, defs)

        return EllipseGenerator(x, y, xrad, yrad, fill, stroke, rotate, clip, children)

class LineGenerator(Generator):
    def __init__(self, x1, y1, x2, y2, stroke=None):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.stroke = stroke

    def generate(self, pw, ph):
        pos1 = Vector2(self.x1.eval(pw, ph), self.y1.eval(pw, ph))
        pos2 = Vector2(self.x2.eval(pw, ph), self.y2.eval(pw, ph))
        return Line(False, pos1, pos2, self.stroke, [], 0)

    @staticmethod
    def from_parse_tree(tree, defs):
        x1 = expression_from_tree(tree.children[0].children[0])
        y1 = expression_from_tree(tree.children[0].children[1])
        x2 = expression_from_tree(tree.children[1].children[0])
        y2 = expression_from_tree(tree.children[1].children[1])
        
        stroke = Generator.stroke_from_tree(tree, defs)

        return LineGenerator(x1, y1, x2, y2, stroke)
        
class PolygonGenerator(Generator):
    def __init__(self, points, fill=None, stroke=None, rotate=0, clip=None, children=[]):
        self.points = points
        self.fill = fill
        self.stroke = stroke
        self.rotate = rotate
        self.clip = clip
        self.children = children

    def generate(self, pw, ph):
        points = [Vector2(P[0].eval(pw, ph), P[1].eval(pw, ph)) for P in self.points]
        xs = [p.x for p in points]
        ys = [p.y for p in points]
        children = self.generate_children(abs(min(xs)-max(xs)), abs(min(ys)-max(ys)))
        return Polygon(self.clip, points, self.stroke, self.fill, children, self.rotate)

    @staticmethod
    def from_parse_tree(tree, defs):
        points = []
        for T in tree.children:
            if T.data == ATTRIBS.POSITION.value:
                points.append((expression_from_tree(T.children[0]), expression_from_tree(T.children[1])))

        children = Generator.children_from_tree(tree, defs)
        fill = Generator.fill_from_tree(tree, defs)

        Generator.validate_modifiers(tree, (ATTRIBS.ROTATED.value, ATTRIBS.CLIPPED.value, ATTRIBS.OUTLINED.value))
        
        rotate = Generator.rotate_from_tree_modifier(tree, defs)
        clip = Generator.clip_from_tree_modifier(tree, defs)
        stroke = Generator.outline_from_tree_modifier(tree, defs)

        return PolygonGenerator(points, fill, stroke, rotate, clip, children)

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
        if self.height_expr != None:
            height = self.height_expr.eval(pw, ph)
        else:
            height = width * (ih / iw)
        size = Vector2(width, height)
        pos = Vector2(self.x.eval(pw, ph), self.y.eval(pw, ph))
        return Image(self.path, pos, size, [], self.rotate)

    @staticmethod
    def from_parse_tree(tree, defs):
        pos = Generator.find_in_tree(tree, ATTRIBS.POSITION.value)
        x = expression_from_tree(pos[0])
        y = expression_from_tree(pos[1])
        width = expression_from_tree(tree.children[2])

        height = None
        if len(tree.children) > 4:
            height = expression_from_tree(tree.children[3])

        path_tree = Generator.find_in_tree(tree, ATTRIBS.PATH.value)
        path = path_tree[0].value[1:-1]

        Generator.validate_modifiers(tree, (ATTRIBS.ROTATED.value))
        
        rotate = Generator.rotate_from_tree_modifier(tree, defs)

        return ImageGenerator(x, y, width, height, path, rotate)

class TextGenerator(Generator):
    def __init__(self, x, y, text, font, color, align=STATIC_MODIFIER.CENTER, width_expr=None, rotate=0):
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
        if self.align == STATIC_MODIFIER.LEFT:
            align = Anchor.LEFT
        elif self.align == STATIC_MODIFIER.RIGHT:
            align = Anchor.RIGHT

        pos = Vector2(self.x.eval(pw, ph), self.y.eval(pw, ph))
        return Text(self.text, pos, width, align, Baseline.TOP, self.font, None, Fill(self.color, 1), [], self.rotate)

    @staticmethod
    def from_parse_tree(tree, defs):
        data = [x.data for x in tree.children]

        pos = Generator.find_in_tree(tree, ATTRIBS.POSITION.value)
        x = expression_from_tree(pos[0])
        y = expression_from_tree(pos[1])
        color = Generator.color_from_tree(tree, defs)
        font = Generator.font_from_tree(tree, defs)

        width_expr = None
        if ATTRIBS.EXPRESSION.value in data:
            width_expr = expression_from_tree(tree.children[4])

        Generator.validate_modifiers(tree, (ATTRIBS.ROTATED.value, STATIC_MODIFIER.LEFT, STATIC_MODIFIER.CENTER, STATIC_MODIFIER.RIGHT))

        rotate = Generator.rotate_from_tree_modifier(tree, defs)
        align = Generator.align_from_tree_modifier(tree, defs)

        content_tree = Generator.find_in_tree(tree, ATTRIBS.CONTENT.value)
        text = content_tree[0].value[1:-1]

        return TextGenerator(x, y, text, font, color, align, width_expr, rotate)