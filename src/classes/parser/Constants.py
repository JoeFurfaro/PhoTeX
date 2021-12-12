# AUTO-GENERATED FILE. DO NOT MODIFY DIRECTLY
# To regenerate run `python3 ConstantsBuilder.py` form this directory

from enum import Enum

def asList(enum):
    result = []
    for val in enum:
        result.append(val.value)
    return result

class IMG_FORMATS(Enum):
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    SVG = "svg"
    
class DEFAULTS:
	FILL_COLOR = "#000"

class DEFS (Enum):
	 COLOR = "color_definition"
	 FONT = "font_definition"
	 TYPE = "type_definition"
	 CANVAS = "canvas_definition"

class ALIASES (Enum):
	 ADD = "add"
	 SUB = "sub"
	 MUL = "mul"
	 DIV = "div"
	 VALUE = "value"
	 NEG = "neg"
	 UNIT = "unit"

class ATTRIBS (Enum):
	 START = "start"
	 IDENTIFIER = "identifier"
	 HEX_COLOR = "hex_color"
	 FONT_NAME = "font_name"
	 FONT_SIZE = "font_size"
	 FONT_WEIGHT = "font_weight"
	 INT_WIDTH = "int_width"
	 INT_HEIGHT = "int_height"
	 ITEM_LIST = "item_list"
	 FILE_NAME = "file_name"
	 ITEM = "item"
	 COLOR = "color"
	 CLIP = "clip"
	 MODIFIER_LIST = "modifier_list"
	 MODIFIER = "modifier"
	 OUTLINED = "outlined"
	 ROTATED = "rotated"
	 CLIPPED = "clipped"
	 SUM = "sum"
	 PRODUCT = "product"
	 EXPRESSION = "expression"
	 POSITION = "position"
	 SIZE = "size"
	 THICKNESS = "thickness"
	 OPACITY = "opacity"
	 ANGLE = "angle"
	 FONT = "font"
	 CONTENT = "content"
	 PATH = "path"
	 RECT = "rect"
	 CIRCLE = "circle"
	 ELLIPSE = "ellipse"
	 LINE = "line"
	 POLYGON = "polygon"
	 TEXT = "text"
	 IMAGE = "image"
	 CUSTOM = "custom"

class FONT_WEIGHT (Enum):
	 THIN = "thin"
	 REGULAR = "regular"
	 BOLD = "bold"

class CLIP_TYPE (Enum):
	 IN = "in"
	 OUT = "out"

class STATIC_MODIFIER (Enum):
	 LEFT = "left"
	 RIGHT = "right"
	 CENTER = "center"

class UNIT (Enum):
	 H = "h"
	 W = "w"

