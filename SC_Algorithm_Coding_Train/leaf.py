from mathutils import Vector


class Leaf:
    pos = Vector((0.0, 0.0, 0.0))
    reached = False

    def __init__(self, position):
        self.pos = position
        reached = False
