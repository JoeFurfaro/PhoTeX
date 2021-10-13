import Item

class Canvas(Item):
    def __init__(self, file_name : str, file_format : str, size : tuple):
        self.name = file_name
        self.format = file_format
        self.size = size
