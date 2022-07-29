from mathutils import Vector


class Leaf:
    """
    Contains the basic information about each leaf,
    also called "attraction node" on the original
    Space Colonization algorithm by Runions et al.
    """
    pos = Vector((0.0, 0.0, 0.0))
    reached = False

    def __init__(self, position):
        """
        Creates a new leaf.

        :param Vector position: leaf position (3D)
        """
        self.pos = position
        reached = False
