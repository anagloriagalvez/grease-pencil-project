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
from GP_Tree_Addon.SC_Algorithm.branch import Branch
from GP_Tree_Addon.SC_Algorithm.leaf import Leaf
import random
import math


class Tree:
    """
    Class that implements a variation of the Space Colonization algorithm by Runions et al.,
    based on The Coding Train code.
    """
    tree_crown_radius = 0.2
    tree_crown_position = Vector((0, 0, 1.5))
    tree_crown_height = 1.0
    branch_length = 0.8

    influence_radius = 0
    kill_distance = 0

    branches = []
    leaves = []
    original_leaves = []
    first_branch = None

    max_iterations = 100  # Prevents infinite loops

    # Drawing parameters
    max_thickness = 1

    # Tree types
    tree_types = ["ROUNDED", "ELLIPSE", "DOUBLE"]

    def __init__(self, n_leaves, branch_length, influence_radius, kill_distance, tree_crown_radius, tree_crown_height,
                 tree_type, max_iterations, max_thickness):
        """
        Creates a tree and initializes the leaves (attraction nodes) based on the tree type.

        :param int n_leaves: Number of "leaves" of the tree
        :param float branch_length: length of each tree branch
        :param influence_radius: distance needed for the trunk to start reaching the leaves
        :param kill_distance: distance for a leaf to be considered "reached" by a branch
        :param float tree_crown_radius: radius of the tree crown
        :param Vector tree_crown_height: height of the tree crown
        :param str tree_type: tree crown type
        :param int max_iterations: maximum number of iterations allowed (avoids crashing)
        :param float max_thickness: maximum thickness of the branches (the trunk thickness)
        """
        self.control_branch_test = None
        self.branch_length = branch_length
        self.influence_radius = influence_radius
        self.kill_distance = kill_distance
        self.tree_crown_radius = tree_crown_radius
        self.tree_crown_height = tree_crown_height
        self.tree_crown_position = Vector((0, 0, tree_crown_height))
        self.max_iterations = max_iterations
        self.max_thickness = max_thickness
        self.branches = []

        if tree_type not in self.tree_types:
            tree_type = self.tree_types[0]
        self.create_tree_crown(n_leaves=n_leaves, crown_type=tree_type, sphere_radius=self.tree_crown_radius,
                               cloud_centre=self.tree_crown_position)
        self.original_leaves = self.leaves.copy()

    # Tree crown
    def create_spherical_points_cloud(self, n_points, sphere_radius, cloud_centre):
        """
        It creates a spherical crown cloud of points randomly distributed and
        use their position to initialize the tree leaves.

        :param int n_points: number of points (leaves)
        :param float sphere_radius: max radius for the cloud
        :param Vector cloud_centre: Position of the 3D space where the cloud should be
        """

        for i in range(0, n_points):
            radius = random.uniform(0.3, 0.7)
            radius = radius * sphere_radius

            alpha = random.uniform(0, math.pi)
            theta = random.uniform(0, 2 * math.pi)

            point = Vector((
                radius * math.cos(theta) * math.sin(alpha),
                radius * math.sin(theta) * math.sin(alpha),
                radius * math.cos(alpha)
            ))

            # Force it to be near the centre
            point = cloud_centre + point
            leaf = Leaf(position=point)
            self.leaves.append(leaf)

    def create_oblate_points_cloud(self, n_points, sphere_radius, cloud_centre):
        """
        It creates an oblate spherical cloud of points randomly distributed and
        use their position to initialize the tree leaves.

        :param int n_points: number of points (leaves)
        :param float sphere_radius: max radius for the cloud
        :param Vector cloud_centre: Position of the 3D space where the cloud should be
        """

        for i in range(0, n_points):
            radius = random.uniform(0.3, 0.7)
            radius = radius * sphere_radius

            alpha = random.uniform(0, math.pi)
            theta = random.uniform(0, 2 * math.pi)
            eta = random.uniform(0.3, 0.7)

            point = Vector((
                radius * float(math.cosh(eta)) * math.cos(theta) * math.sin(alpha),
                radius * float(math.cosh(eta)) * math.sin(theta) * math.sin(alpha),
                radius * float(math.sinh(eta)) * math.cos(alpha)
            ))

            # Force it to be near the centre
            point = cloud_centre + point
            leaf = Leaf(position=point)
            self.leaves.append(leaf)

    def create_tree_crown(self, n_leaves, crown_type, sphere_radius, cloud_centre):
        """
        Creates the tree crown (initializes the leaves) based on the crown type.

        :param int n_leaves: Max number of leaves
        :param str crown_type: Type of tree crown shape: Rounded, spherical, double
        :param float sphere_radius: Determines the size of the crown
        :param float cloud_centre: Where the crown centre should be placed
        """
        if crown_type == "ROUNDED":
            self.create_spherical_points_cloud(n_points=n_leaves, sphere_radius=sphere_radius,
                                               cloud_centre=cloud_centre)
        elif crown_type == "ELLIPSE":
            self.create_oblate_points_cloud(n_points=n_leaves, sphere_radius=sphere_radius,
                                            cloud_centre=cloud_centre)
        elif crown_type == "DOUBLE":
            n_leaves = int(n_leaves / 2)
            cloud_centre_1 = self.tree_crown_position + Vector((-0.33 * self.tree_crown_height, 0, 0))
            cloud_centre_2 = self.tree_crown_position + \
                             Vector((0.2 * self.tree_crown_height, 0, 0.33 * self.tree_crown_height))

            self.create_oblate_points_cloud(n_points=n_leaves, sphere_radius=sphere_radius / 1.2,
                                            cloud_centre=cloud_centre_1)
            self.create_oblate_points_cloud(n_points=n_leaves, sphere_radius=sphere_radius,
                                            cloud_centre=cloud_centre_2)

    # Tree trunk
    def create_trunk(self):
        """
        Aux method to create the tree's trunk. It keeps growing (creating new branches)
        towards the same direction (up) until it's close enough to the leaves
        """
        self.first_branch = Branch(position=Vector((0, 0, 0)), direction=Vector((0, 0, 1)), length=self.branch_length,
                                   thickness=self.max_thickness, parent=None)
        self.branches.append(self.first_branch)
        current_branch = self.first_branch

        while not self.trunk_close_enough(current_branch):
            trunk = Branch(position=current_branch.pos + current_branch.direction * current_branch.length,
                           direction=current_branch.direction.copy(),
                           parent=current_branch, length=self.branch_length, thickness=current_branch.thickness * 0.97)
            current_branch.children.append(trunk)
            self.branches.append(trunk)
            current_branch = trunk

    def trunk_close_enough(self, branch):
        """
        Aux method used to check if the new trunk branches are close
        enough to any leaf.

        :param Branch branch: the branch used to check if it's close enough
        """
        for leaf in self.leaves:
            if (leaf.pos - branch.pos).length < self.influence_radius:
                return True

    # Auxiliary method
    def generate_random_direction(self):
        """
        An aux method used to create a random direction (normalized vector)
        :return:
        Vector direction: random direction vector
        """
        alpha = random.uniform(0, math.pi)
        theta = random.uniform(0, 2 * math.pi)

        direction = Vector((
            math.cos(theta) * math.sin(alpha),
            math.sin(theta) * math.sin(alpha),
            math.cos(alpha)
        ))

        direction.normalize()

        return direction

    # Main algorithm
    def generate_tree(self):
        """
        Core of the Space Colonization algorithm.
        :return:
        True if the tree has been correctly generated
        False if there have been some problem while creating the tree
        """
        if self.leaves == 0 or not self.leaves:
            return False

        self.create_trunk()
        # Main growing algorithm
        n_iterations = 0

        while len(self.leaves) > 0 and n_iterations < self.max_iterations:
            for leaf in self.leaves:
                closest_branch = None
                closest_direction = None
                record_distance = -1

                for branch in self.branches:
                    _branch_end = branch.pos + branch.length * branch.direction
                    direction = leaf.pos - _branch_end
                    distance = direction.length

                    if distance <= self.kill_distance:
                        leaf.reached = True
                        closest_branch = None
                        break

                    elif closest_branch is None or distance < record_distance:
                        closest_branch = branch
                        closest_direction = direction
                        record_distance = distance

                # We've found a close enough branch
                if closest_branch is not None:
                    closest_direction.normalize()
                    closest_branch.direction = closest_branch.direction + closest_direction
                    closest_branch.count = closest_branch.count + 1

            # Clear reached leaves
            _non_reached_leaves = []
            for leaf in self.leaves:
                if leaf.reached is False:
                    _non_reached_leaves.append(leaf)

            self.leaves.clear()
            self.leaves = _non_reached_leaves

            _new_branches = []
            for branch in self.branches:
                # If there's a leaf attracting, create new branch towards it
                if branch.count > 0:
                    branch.direction = branch.direction / branch.count
                    branch.direction.normalize()
                    _new_branch_direction = branch.direction.copy() + self.generate_random_direction() * 0.1

                    # Re-do this method as we can simply calculate the new branch direction without modifying the
                    # current branch's one
                    branch.reset()

                    _new_branch = Branch(position=branch.pos + branch.length * branch.direction,
                                         direction=_new_branch_direction, parent=None,
                                         length=branch.length, thickness=branch.thickness * 0.98)

                    branch.children.append(_new_branch)
                    _new_branches.append(_new_branch)
                    self.control_branch_test = _new_branch

            self.branches.extend(_new_branches)

            n_iterations = n_iterations + 1

        return True
