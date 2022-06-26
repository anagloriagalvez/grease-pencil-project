import sys

sys.path.append(r"C:\Users\Ana Gloria\Desktop\TFG\grease-pencil-project\SC_Algorithm")
import bpy
from mathutils import Vector
from branch import Branch
# from .branch import Branch
import math
import random


class SCTree:
    # Cloud of points generation
    n_leaves = 10
    cloud_radius = 0.3

    # Algorithm parameters
    start_pos = Vector((0.0, 0.0, 0.0))
    branch_length = 0.5
    attraction_distance = 0.2
    reach_distance = 0.7

    leaves = []
    original_leaves = [] # In order to draw them
    leaves_attracting = []

    first_branch = None
    branches = []
    extreme_branches = []

    def __init__(self, n_leaves, branch_length, attraction_distance,
                 reach_distance):  # Add tree type in order to generate different cloud of points
        self.n_leaves = n_leaves
        self.branch_length = branch_length
        self.attraction_distance = attraction_distance
        self.reach_distance = reach_distance

    def create_spherical_points_cloud(self, n_points, sphere_radius, cloud_centre):
        points_cloud = []
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
            points_cloud.append(point)

        return points_cloud

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

    def remove_reached_leaves(self):
        for leaf in reversed(self.leaves):
            for branch in self.branches:
                if (branch.end - leaf).length <= self.reach_distance:
                    self.leaves.remove(leaf)
                    break;

    def clear_leaves_attracting(self):
        self.leaves_attracting.clear()
        for branch in self.branches:
            branch.leaves_attracting.clear()

    def find_leaves_attracting(self):
        for leaf in self.leaves:
            record_distance = 99999
            closest_branch = None

            for branch in self.branches:
                distance = (branch.end - leaf).length

                # Look for the closest branch within the attraction distance
                if distance <= self.attraction_distance and distance < record_distance:
                    record_distance = distance
                    closest_branch = branch

            # If any branch is attracted by the leaf, we add it to attracting leaves
            if closest_branch is not None:
                closest_branch.leaves_attracting.append(leaf)
                self.leaves_attracting.append(leaf)

    def generate_tree(self):

        # Creation of leaves (points cloud)
        self.leaves = self.create_spherical_points_cloud(n_points=self.n_leaves, sphere_radius=self.cloud_radius, cloud_centre=Vector((0, 0, 1.5)))
        self.original_leaves = self.leaves.copy()

        # First branch creation -> special, no parent
        self.first_branch = Branch(start=self.start_pos, end=self.start_pos + Vector((0, 0, self.branch_length)),
                                   direction=Vector((0, 0, 1)), parent=None)
        self.branches.append(self.first_branch)
        self.extreme_branches.append(self.first_branch)

        main_loop_iterations = 0
        # Algorithm main loop
        while len(self.leaves) > 0:

            self.remove_reached_leaves()

            if len(self.leaves) > 0:

                # Clear leaves attracting and calculate them again as new branches have been generated
                self.clear_leaves_attracting()

                # Calculate new leaves attracting branches
                self.find_leaves_attracting()

            # If any leaf is attracting branches, we force the branches grow towards them
            if len(self.leaves_attracting) > 0:
                print("AMOUNT OF LEAVES ATTRACTING:{}".format(self.leaves_attracting))
                print(len(self.leaves_attracting))

                self.extreme_branches.clear()
                _new_branches = []

                for branch in self.branches:
                    print("AMOUNT OF BRANCHES: {}".format(len(self.branches)))
                    if len(branch.leaves_attracting) > 0:
                        # Medium direction among all the attracting leaves
                        _new_dir = Vector((0, 0, 0))

                        for attracting_leaf in branch.leaves_attracting:
                            _attracting_dir = attracting_leaf - branch.end
                            _attracting_dir.normalize()

                            _new_dir = _new_dir + _attracting_dir

                        _new_dir = _new_dir / len(branch.leaves_attracting)
                        _new_dir = _new_dir + self.generate_random_direction() * 0.05 # Arbitrary value
                        _new_dir.normalize()

                        # Variation! Reduce branch length if we are closer to the leaf
                        _new_branch = Branch(start=branch.end, end=branch.end + _new_dir * self.branch_length/2,
                                             direction=_new_dir, parent=branch)
                        branch.children.append(_new_branch)
                        _new_branches.append(_new_branch)
                        self.extreme_branches.append(_new_branch)

                    else:  # If the branch it's not attracted, check if it's an extreme
                        if len(branch.children) == 0:
                            self.extreme_branches.append(branch)

                print("NEW BRANCHES GENERATED: {}".format(len(_new_branches)))
                self.branches.extend(_new_branches)

            # If no leaves are attracting branches (but we still have leaves), tree extremities branches should grow
            # towards the same direction (e.g.: Trunk)
            else:
                for ex_branch in reversed(self.extreme_branches):
                    _new_branch = Branch(start=ex_branch.end,
                                         end=ex_branch.end + ex_branch.direction * self.branch_length,
                                         direction=ex_branch.direction, parent=ex_branch)
                    ex_branch.children.append(_new_branch)
                    self.branches.append(_new_branch)
                    self.extreme_branches.append(_new_branch)

            main_loop_iterations = main_loop_iterations + 1
            print(main_loop_iterations)
            if main_loop_iterations >= 10:
                break;

        print("First branch children: {}".format(self.first_branch.children))