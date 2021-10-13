import Item

class Image(Item):

    def __init__(self, path : str, size : tuple, position : tuple):
        self.path = path
        self.size = size
        self.pos = position
