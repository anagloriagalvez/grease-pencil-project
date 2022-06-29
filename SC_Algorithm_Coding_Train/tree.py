import sys

sys.path.append(r"C:\Users\Ana Gloria\Desktop\TFG\grease-pencil-project\SC_Algorithm_Coding_Train")

from mathutils import Vector
from branch import Branch
from leaf import Leaf
import random
import math


class Tree:
    branches_sphere_radius = 0.2
    tree_height = 0.8

    max_dist = 0
    min_dist = 0

    branches = []
    leaves = []
    original_leaves = []

    # Drawing parameters
    max_thickness = 1

    def __init__(self, n_leaves, tree_height, max_dist, min_dist, max_thickness):
        self.branches = []
        self.create_spherical_points_cloud(n_points=n_leaves, sphere_radius=self.branches_sphere_radius,
                                           cloud_centre=Vector((0, 0, 0.5)))
        self.original_leaves = self.leaves.copy()
        self.tree_height = tree_height
        self.max_dist = max_dist
        self.min_dist = min_dist
        self.max_thickness = max_thickness

    def create_trunk(self):
        root = Branch(position=Vector((0, 0, 0)), direction=Vector((0, 0, 1)), length=self.tree_height, thickness=self.max_thickness)
        self.branches.append(root)
        current_branch = root

        while not self.trunk_close_enough(current_branch):
            trunk = Branch(position=current_branch.pos + current_branch.direction * current_branch.length,
                           direction=current_branch.direction.copy(),
                           parent=current_branch, length=self.tree_height, thickness=current_branch.thickness * 0.90)
            self.branches.append(trunk)
            current_branch = trunk

    def trunk_close_enough(self, branch):
        for leaf in self.leaves:
            if (leaf.pos - branch.pos).length < self.max_dist:
                return True

    def create_spherical_points_cloud(self, n_points, sphere_radius, cloud_centre):
        for i in range(0, n_points):
            radius = random.uniform(0.5, 1)
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
            _new_leaf = Leaf(position=point)
            self.leaves.append(_new_leaf)

    def generate_random_direction(self):
        alpha = random.uniform(0, math.pi)
        theta = random.uniform(0, 2 * math.pi)

        direction = Vector((
            math.cos(theta) * math.sin(alpha),
            math.sin(theta) * math.sin(alpha),
            math.cos(alpha)
        ))

        direction.normalize()

        return direction

    def generate_tree(self):
        self.create_trunk()

        # Main growing algorithm
        n_iterations = 0

        while len(self.leaves) > 0:
            for leaf in self.leaves:
                closest_branch = None
                closest_direction = None
                record_distance = -1

                for branch in self.branches:
                    _branch_end =branch.pos + branch.length * branch.direction
                    direction = leaf.pos - _branch_end
                    distance = direction.length

                    if distance <= self.min_dist:
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
                                         length=branch.length, thickness=branch.thickness * 0.80)
                    _new_branches.append(_new_branch)
                    self.control_branch_test = _new_branch

            self.branches.extend(_new_branches)

            n_iterations = n_iterations + 1
            if n_iterations > 100:
                print("N_LEAVES: {}".format(len(self.leaves)))
                break
