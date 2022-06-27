from mathutils import Vector

class Branch:
    parent = None
    pos = Vector((0.0, 0.0, 0.0))
    direction = Vector((0.0, 0.0, 0.0))
    direction_bkp = Vector((0.0, 0.0, 0.0))
    children = 0
    length = 0.2

    def __init__(self, position, direction, parent=None):
        if parent:
            self.parent = parent
            self.pos = parent.next()
            self.direction = parent.direction.copy()
            self.direction_bkp = direction.copy()
        else:
            self.parent = None
            self.pos = position.copy()
            self.direction = direction.copy()
            self.direction_bkp = direction.copy()
        self.children = 0
        self.length = 0.2

    def reset(self):
        self.children = 0
        self.direction = self.direction_bkp.copy()

    def next(self):
        next_post = self.pos + self.direction * self.length
        return next_post





