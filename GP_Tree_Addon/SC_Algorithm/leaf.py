# -----------------------------------------------------------
# Code based on The Coding Train implementation
# Released under MIT License
# Link to GitHub:
# https://github.com/CodingTrain/Coding-Challenges/tree/main/018_SpaceColonizer3D/Processing/CC_018_SpaceColonizer3D
# Link to webpage:
# https://thecodingtrain.com/challenges/17-fractal-trees-space-colonization
#
# Blender + Python adaptation by: Ana Gloria Gálvez Mellado
# ana.gloria.galvez99@gmail.com
# -----------------------------------------------------------
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
