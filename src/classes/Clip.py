class Clip(object):
    def __init__(self, clipped_in : bool=True):
        self.clipped_in = clipped_in

    def is_inner(self):
        return self.clipped_in

    def is_outer(self):
        return not self.clipped_in