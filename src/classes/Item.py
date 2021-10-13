class Item():
    def __init__(self, parent, children : list(), rotation : float):
        self.parent = parent
        self.child = children
        self.rot = rotation

    def __init__(self, parent, children):
        self.parent = parent
        self.child = children
        self.rot = 0

