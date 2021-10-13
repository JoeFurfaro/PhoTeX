import Item, Font

class Text(Item):

    def __init__(self, text : str, font : Font, color, align : str, position : tuple, width):
        self.text = text
        self.font = font
        self.color = color
        self.align = align
        self.pos = position
        self.width = width