class DefLookup:

    def __init__(self):
        self.colors = []
        self.fonts = []
        self.types = []
        self.canvases = []

class ColorDef:

    def __init__(self, ID : str, hex : str):
        self.ID = ID
        self.hex = hex