import Polygon

class Line(Polygon):

    def __init__(self, start : tuple, end : tuple):
        self.start = start
        self.end = end