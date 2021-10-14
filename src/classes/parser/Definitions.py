class ColorDef:
    def __init__(self, ID : str, hex : str):
        self.ID = ID # Identifier
        self.hex = hex # Hex code in the form "#AAAAAA"

class FontDef:
    def __init__(self, ID : str, font_name : str, font_size : int, font_weight : str = "regular"):
        self.ID = ID # Identifier
        self.font_name = font_name # Font name
        self.font_size = font_size # Font size

class TypeDef:
    def __init__(self, ID : str, width : int = None, height : int = None):
        self.ID = ID # Identifier
        self.width = width # Preset width of rect
        self.height = height # Preset height of rect
        self.tree = [] # Tree of finalized objects the type contains

class CanvasDef:
    def __init__(self, file : str, width : int, height : int):
        self.file = file # File name to export to
        self.width = width # Width of canvas
        self.height = height # Height of canvas
        self.tree = [] # Tree of finalized objects the canvas contains

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

    # Check if a font with a given identifier exists
    def has_font(self, ID):
        return any([x.ID == ID for x in self.fonts])

    # Check if a type with a given identifier exists
    def has_type(self, ID):
        return any([x.ID == ID for x in self.types])

    # Check if a canvas with a given file name exists
    def has_type(self, file):
        return any([x.file == file for x in self.canvases])