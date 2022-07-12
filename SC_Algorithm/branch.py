# -----------------------------------------------------------
# Code based on The Coding Train implementation
# Released under MIT License
# Link to GitHub: shorturl.at/CFMQY
# Link to webpage: shorturl.at/cWY16
#
# Blender + Python adaptation by: Ana Gloria Gálvez Mellado
# ana.gloria.galvez99@gmail.com
# -----------------------------------------------------------
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
    length = 0

    # Drawing parameters
    thickness = 1

    def __init__(self, position, direction, parent, length, thickness):
        """
        Creates a new branch.

        :param Vector position: original branch position
        :param Vector direction: growth direction of the branch
        :param Branch parent: the branch's parent (another branch)
        :param float length: branch's length
        :param float thickness: branch thickness (with drawing purposes)
        """
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
        """
        Clears the count and resets the direction, used to
        calculate the new branch's average direction on the
        main algorithm.
        """
        self.count = 0
        self.direction = self.direction_bkp.copy()
