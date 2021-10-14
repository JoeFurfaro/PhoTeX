# Shape interface
import Item

class Shape(Item):

    #Where to put the super constructor?
    def __init__(self, stroke, fill, clipped: bool):
        self.stroke = stroke
        self.fill = fill
        self.clipped = clipped

    def render(self) -> str:
        raise NotImplementedError