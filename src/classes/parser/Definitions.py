from ..Font import Font
from ..parser.Generators import *
from ..Canvas import Canvas
from ..util.Vector2 import Vector2

class ColorDef:
    def __init__(self, ID : str, hex : str):
        self.ID = ID # Identifier
        self.hex = hex # Hex code in the form "#AAAAAA"

class FontDef:
    def __init__(self, ID : str, font_name : str, font_size : int, font_weight : str = "regular"):
        self.ID = ID # Identifier
        self.font_name = font_name # Font name
        self.font_size = font_size # Font size
        self.font_weight = font_weight # Font weight
        self.obj = Font(font_name, font_size, font_weight)

class TypeDef:
    def __init__(self, ID : str, width : int = None, height : int = None, children_generators = []):
        self.ID = ID # Identifier
        self.width = width # Preset width of rect
        self.height = height # Preset height of rect
        self.children_generators = children_generators # Tree of finalized objects the type contains

    def has_preset_size(self):
        return self.width != None and self.height != None

    def construct_generator(self, x, y, width, height): # All are Expressions
        return RectGenerator(x, y, width, height, children=self.children_generators)

class CanvasDef:
    def __init__(self, base : str, ext : str, width : int, height : int, children_generators = []):
        self.name = base + "." + ext
        self.base = base # File name to export to
        self.ext = ext # File extension to export to
        self.width = width # Width of canvas
        self.height = height # Height of canvas
        self.children_generators = children_generators # Tree of finalized objects the canvas contains
        self.children = None

    def generate(self):
        self.children = []
        for gen in self.children_generators:
            self.children.append(gen.generate(self.width, self.height))

class DefLookup:
    def __init__(self):
        self.colors = []
        self.fonts = []
        self.types = []
        self.canvases = []

    def add(self, x):
        if type(x) == ColorDef:
            self.colors.append(x)
        elif type(x) == FontDef:
            self.fonts.append(x)
        elif type(x) == TypeDef:
            self.types.append(x)
        elif type(x) == CanvasDef:
            self.canvases.append(x)
        else: 
            raise TypeError("Attempted to add something that is not a definition to the definition lookup table")

    # Check if a color with a given identifier exists
    def has_color(self, ID):
        return any([x.ID == ID for x in self.colors])

    def get_color(self, ID):
        for x in self.colors:
            if x.ID == ID:
                return x.hex
        return None

    # Check if a font with a given identifier exists
    def has_font(self, ID):
        return any([x.ID == ID for x in self.fonts])

    def get_font(self, ID):
        for x in self.fonts:
            if x.ID == ID:
                return x
        return None

    # Check if a type with a given identifier exists
    def has_type(self, ID):
        return any([x.ID == ID for x in self.types])

    def get_type(self, ID):
        for x in self.types:
            if x.ID == ID:
                return x
        return None

    # Check if a canvas with a given file name exists
    def has_canvas(self, name):
        return any([x.name == name for x in self.canvases])
