# Shape interface
import Item

class Shape(Item):

    #Where to put the super constructor?
    def __init__(self, stroke, fill, clipped: bool):
        self.stroke = stroke
        self.fill = fill
        self.clipped = clipped

    def validate(self, properties: dict) -> bool:
        raise NotImplementedError

    def render(self) -> str:
        raise NotImplementedError