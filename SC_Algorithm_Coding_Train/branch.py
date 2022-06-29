from mathutils import Vector

class Branch:
    parent = None
    pos = Vector((0.0, 0.0, 0.0))
    direction = Vector((0.0, 0.0, 0.0))
    direction_bkp = Vector((0.0, 0.0, 0.0))
    count = 0
    length = 0.2

    # Drawing parameters
    thickness = 1

    def __init__(self, position, direction, parent=None, length=0.2, thickness=1):
        self.parent = parent
        self.pos = position.copy()
        self.direction = direction.copy()
        self.direction_bkp = direction.copy()
        self.length = length
        self.count = 0
        self.thickness = thickness

    def reset(self):
        self.count = 0
        self.direction = self.direction_bkp.copy()





