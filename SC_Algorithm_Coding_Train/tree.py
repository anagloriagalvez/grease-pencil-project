import sys

sys.path.append(r"C:\Users\Ana Gloria\Desktop\TFG\grease-pencil-project\SC_Algorithm_Coding_Train")

from mathutils import Vector
from branch import Branch
from leaf import Leaf
import random
import math


class Tree:
    branches_sphere_radius = 0.24
    tree_height = 0.8

    max_dist = 0
    min_dist = 0

    branches = []
    leaves = []

    def __init__(self, n_leaves, tree_height, max_dist, min_dist):
        self.branches = []
        self.create_spherical_points_cloud(n_points=n_leaves, sphere_radius=self.branches_sphere_radius,
                                           cloud_centre=Vector((0, 0, 0.5)))
        self.tree_height = tree_height
        self.max_dist = max_dist
        self.min_dist = min_dist

    def create_trunk(self):
        root = Branch(position=Vector((0, 0, self.tree_height / 2)), direction=Vector((0, 0, 1)))
        self.branches.append(root)
        current_branch = root

        while not self.trunk_close_enough(current_branch):
            trunk = Branch(position=current_branch.next().copy(), direction=current_branch.direction.copy(),
                           parent=current_branch)
            self.branches.append(trunk)
            current_branch = trunk

    def trunk_close_enough(self, branch):
        for leaf in self.leaves:
            if leaf.pos - branch.pos < self.max_dist:
                return True

    def create_spherical_points_cloud(self, n_points, sphere_radius, cloud_centre):
        for i in range(0, n_points):
            radius = random.uniform(0, 1)
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

    def generate_tree(self):
        self.create_trunk()

        # Main growing algorithm
        n_iterations = 0

        while len(self.leaves) > 0 or n_iterations > 10:
            for leaf in self.leaves:
                closest_branch = None
                closest_direction = None
                record_distance = 99999

                for branch in self.branches:
                    direction = leaf.pos - branch.pos
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

                    _new_branch = Branch(position=branch.next().copy(), direction=branch.direction.copy(), parent=branch)
                    _new_branches.append(_new_branch)

                    # Re-do this method as we can simply calculate the new branch direction without modifying the
                    # current branch's one
                    branch.reset()

            self.branches.extend(_new_branches)

            n_iterations = n_iterations + 1