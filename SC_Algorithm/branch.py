from mathutils import Vector


class Branch:
    """
    Contains the information about every branch, also called "tree node"
    on the original Space Colonization algorithm by Runions et al.
    """
    parent = None
    children = []
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
        # Reset children
        self.children = []

    def reset(self):
        self.count = 0
        self.direction = self.direction_bkp.copy()
