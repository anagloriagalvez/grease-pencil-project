# -----------------------------------------------------------
# Code based on The Coding Train implementation
# Released under MIT License
# Link to GitHub: shorturl.at/CFMQY
# Link to webpage: shorturl.at/cWY16
#
# Blender + Python adaptation by: Ana Gloria Gálvez Mellado
# ana.gloria.galvez99@gmail.com
# -----------------------------------------------------------

import sys

sys.path.append(r"C:\Users\Ana Gloria\Desktop\TFG\grease-pencil-project\SC_Algorithm")
import bpy
from mathutils import Vector
import random
from tree import Tree


def do_main():
    # reach_distance < branch_length < attraction_distance
    my_tree = Tree(n_leaves=150, branch_length=0.02, max_dist=0.3, min_dist=0.02, tree_crown_radius=1,
                   tree_crown_position=Vector((0, 0, 1.5)), max_iterations=50, max_thickness=80)
    my_tree.generate_tree()

    draw_tree(my_tree)
    draw_leaves(my_tree)


def draw_tree(tree):
    gp_layer = init_grease_pencil()
    gp_frame = gp_layer.frames.new(0)

    #draw_recursive(gp_frame=gp_frame, point_list=[], branch=tree.first_branch)

    for branch in tree.branches:
        draw_line(gp_frame, branch.pos, branch.pos + branch.direction * branch.length, branch.thickness)


def draw_leaves(tree):
    for leaf in tree.original_leaves:
        bpy.ops.mesh.primitive_uv_sphere_add(location=leaf.pos, radius=0.025)


def get_grease_pencil(gpencil_obj_name='GPencil') -> bpy.types.GreasePencil:
    """
    Return the grease-pencil object with the given name. Initialize one if not already present.
    :param gpencil_obj_name: name/key of the grease pencil object in the scene
    """

    # If not present already, create grease pencil object
    if gpencil_obj_name not in bpy.context.scene.objects:
        bpy.ops.object.gpencil_add(location=(0, 0, 0), type='EMPTY')
        # rename grease pencil
        bpy.context.scene.objects[-1].name = gpencil_obj_name

    # Get grease pencil object
    gpencil = bpy.context.scene.objects[gpencil_obj_name]

    return gpencil


def get_grease_pencil_layer(gpencil: bpy.types.GreasePencil, gpencil_layer_name='GP_Layer',
                            clear_layer=False) -> bpy.types.GPencilLayer:
    """
    Return the grease-pencil layer with the given name. Create one if not already present.
    :param gpencil: grease-pencil object for the layer data
    :param gpencil_layer_name: name/key of the grease pencil layer
    :param clear_layer: whether to clear all previous layer data
    """

    # Get grease pencil layer or create one if none exists
    if gpencil.data.layers and gpencil_layer_name in gpencil.data.layers:
        gpencil_layer = gpencil.data.layers[gpencil_layer_name]
    else:
        gpencil_layer = gpencil.data.layers.new(gpencil_layer_name, set_active=True)
        gpencil_layer.line_change = 500

    if clear_layer:
        gpencil_layer.clear()  # clear all previous layer data

    # bpy.ops.gpencil.paintmode_toggle()  # need to trigger otherwise there is no frame

    return gpencil_layer


# Util for default behavior merging previous two methods
def init_grease_pencil(gpencil_obj_name='GPencil', gpencil_layer_name='GP_Layer',
                       clear_layer=True) -> bpy.types.GPencilLayer:
    gpencil = get_grease_pencil(gpencil_obj_name)
    gpencil_layer = get_grease_pencil_layer(gpencil, gpencil_layer_name, clear_layer=clear_layer)
    return gpencil_layer


def draw_recursive(gp_frame, point_list, branch):
    print("CHILDREN: {}".format(len(branch.children)))

    point = [branch.pos, branch.thickness]
    point_list.append(point)

    if len(branch.children) == 0:
        draw_line_n_points(gp_frame, points_list=point_list)
        print("TRUE")
        return

    point = [branch.children[0].pos, branch.children[0].thickness]
    point_list.append(point)

    draw_recursive(gp_frame=gp_frame, point_list=point_list, branch=branch.children[0])

    if len(branch.children) > 1:
        print("HELLO")
        print("--CHILDREN: {}".format(len(branch.children)))
        for i in range(1, len(branch.children)):
            new_point_list = []
            point = [branch.pos, branch.thickness]
            point_list.append(point)

            draw_recursive(gp_frame=gp_frame, point_list=new_point_list, branch=branch.children[i])

def draw_line_n_points(gp_frame, points_list):
    # Init new stroke
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'  # allows for editing


    # Define stroke geometry
    gp_stroke.points.add(count=len(points_list))
    for count, point in enumerate(points_list):
        gp_stroke.points[count].co = point[0]
        gp_stroke.points[count].pressure = point[1]

def draw_line(gp_frame, p0: tuple, p1: tuple, thickness=1):
    # Init new stroke
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'  # allows for editing

    # Define stroke geometry
    gp_stroke.points.add(count=2)
    gp_stroke.points[0].co = p0
    gp_stroke.points[0].pressure = thickness
    gp_stroke.points[1].co = p1
    gp_stroke.points[1].pressure = thickness
    return gp_stroke


# test
do_main()
