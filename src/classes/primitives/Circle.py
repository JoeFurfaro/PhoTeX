import Ellipse

class Circle(Ellipse):

    # create circle as an ellipse with same x and y radius
    def __init__(self, position : tuple, radius : float):
        super().__init__(self, position, radius, radius)