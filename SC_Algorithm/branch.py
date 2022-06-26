from mathutils import Vector


class Branch:
    start = Vector((0.0, 0.0, 0.0))
    end = Vector((0.0, 0.0, 0.0))
    direction = Vector((0.0, 0.0, 0.0))
    parent = None
    children = []
    leaves_attracting = []
    #grown = False

    def __init__(self, start, end, direction, parent):
        self.start = start
        self.end = end
        self.direction = direction
        self.parent = parent

        # Reset children
        self.children = []
        self.leaves_attracting = []
