import bpy
import os
from mathutils import *
import math
from .SC_Algorithm.tree import Tree
import random


# AUX

def generate_random_direction():
    """
    An aux method used to create a random direction (normalized vector)
    :return:
    Vector direction: Random direction vector
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


# GREASE PENCIL GETTERS

def get_gp_object(name='GPencil', create_new=True):
    """
    Create or get a Grease Pencil object, based on the name
    :param str name: Name of the Grease Pencil object
    :param bool create_new: False if the object already exist, and
                            we want to search it on the scene
    :return:
    grease pencil object: Reference to the gp object inside Blender
    """

    # If not in scene, add a new object
    if name not in bpy.context.scene.objects or create_new:
        bpy.ops.object.gpencil_add(type="EMPTY")
        # Change name
        bpy.context.selected_objects[0].name = name
        real_name = bpy.context.selected_objects[0].name
    return bpy.context.scene.objects[real_name]


def get_gp_layer(gp_object=None, layer_name="Layer", clear_layer=False):
    """
    Create or get a Grease Pencil layer (inside GP object)
    :param gp_object: Reference to the gp object inside Blender
    :param str layer_name: Layer name
    :param bool clear_layer: True if the layer should be cleared (empty)
    :return:
    grease pencil layer: Reference to the gp layer inside Blender
    """
    if layer_name in gp_object.data.layers.keys():  # List of layer names
        gpencil_layer = gp_object.data.layers[layer_name]
        if clear_layer:
            gpencil_layer.clear()
        return gpencil_layer
    return gp_object.data.layers.new(name=layer_name, set_active=True)


def get_frame_gp_layer(gp_layer=None, frame_number=0):
    """
    Create or get a Grease Pencil frame (inside GP layer)
    :param gp_layer: Reference to the gp layer inside Blender
    :param frame_number: Number of the frame we want to create
    :return:
    grease pencil frame: Reference to the gp frame inside Blender
    """
    for index, frame in enumerate(gp_layer.frames):
        if frame.frame_number == frame_number:
            return gp_layer.frames[index]
    # If not found, return new frame
    return gp_layer.frames.new(frame_number)


# ASPECT-RELATED METHODS: MATERIALS

def import_image(image_path=None):
    """
    Import image to Blender, so it can be used
    through the Blender API.
    :param str image_path: Full path of the image
    :return:
    image: Image object in Blender
    """
    image = bpy.data.images.load(filepath=image_path)

    return image


def create_material_texture(material_name="New Texture Material", color=(0.0, 0.0, 0.0, 1.0), mode='DOTS',
                            text_img=None):
    """
    Create a Grease Pencil material with a texture (image) and a color.
    :param str material_name: Name of the new material
    :param Tuple color: R, G, B, A values of the new color
    :param str mode: Line type ('LINEAR', 'DOTS', 'SQUARES')
    :param image text_img: Blender image (used for the texture)
    :return:
    gp_mat: Reference to the material inside Blender
    """

    gp_mat = bpy.data.materials.new(material_name)
    bpy.data.materials.create_gpencil_data(gp_mat)
    gp_mat.grease_pencil.color = color
    gp_mat.grease_pencil.show_stroke = True
    gp_mat.grease_pencil.mode = mode
    gp_mat.grease_pencil.stroke_style = 'TEXTURE'
    gp_mat.grease_pencil.stroke_image = text_img
    gp_mat.grease_pencil.mix_stroke_factor = 1.0
    gp_mat.grease_pencil.alignment_mode = 'PATH'
    gp_mat.grease_pencil.show_fill = False

    return gp_mat


def create_material_color(material_name="New Color Material", color=(0.0, 0.0, 0.0, 1.0), mode='LINE'):
    """
    Create a Grease Pencil material with a given color.
    :param str material_name: Name of the new material
    :param Tuple color: R, G, B, A values of the new color
    :param str mode: Line type ('LINEAR', 'DOTS', 'SQUARES')
    :return:
    gp_mat: Reference to the material inside Blender
    """
    gp_mat = bpy.data.materials.new(material_name)
    bpy.data.materials.create_gpencil_data(gp_mat)
    gp_mat.grease_pencil.color = color
    gp_mat.grease_pencil.show_stroke = True
    gp_mat.grease_pencil.mode = mode
    gp_mat.grease_pencil.stroke_style = 'SOLID'
    gp_mat.grease_pencil.mix_stroke_factor = 1.0
    gp_mat.grease_pencil.show_fill = False

    return gp_mat


def add_active_material_to_gp(gp_object=None, material_to_add=None):
    """
    Change the "active material" of a GP object, so it can be used to draw
    :param gp_object: Reference to the gp object inside Blender
    :param material_to_add: Reference to the gp material inside Blender
    """
    gp_object.data.materials.append(material_to_add)
    gp_object.active_material = material_to_add


# MAIN DRAWING METHOD
def apply_custom_vertex_config_leaves(point=None):
    """
    For a given point (of a stroke), the color and UV rotation properties are
    randomly modified (on a controlled range) so different shadows of a green
    color are obtained, achieving a more interesting look on the leaves.
    :param point: Reference to the gp point (of a stroke) inside Blender
    """
    point.vertex_color.data.vertex_color[0] = random.uniform(0.300, 0.350)  # Hue
    point.vertex_color.data.vertex_color[1] = 0.502  # Saturation
    point.vertex_color.data.vertex_color[2] = random.uniform(0.200, 0.300)  # Value
    point.vertex_color.data.vertex_color[3] = random.uniform(0.0, 1.0) # Mix factor


def draw_line(gp_frame=None, p0=Vector((0, 0, 0)), p1=Vector((0, 0, 0)), thickness=1):
    """
    Create a new stroke with 2 points (straight line) inside a given gp frame
    :param gp_frame: Reference to the gp frame inside Blender
    :param Vector p0: Position of the first point of the line
    :param Vector p1: Position of the second point of the line
    :param thickness: Line thickness
    :return:
    grease pencil stroke: Reference to the gp stroke inside Blender
    """

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


def draw_line_custom_leaves(gp_frame=None, p0=Vector((0, 0, 0)), p1=Vector((0, 0, 0)), thickness=1):
    """
    Create a new stroke with 2 points (straight line) inside a given gp frame.
    Apply a special per-vertex configuration for textured leaves to look better.
    :param gp_frame: Reference to the gp frame inside Blender
    :param Vector p0: Position of the first point of the line
    :param Vector p1: Position of the second point of the line
    :param thickness: Line thickness
    :return:
    grease pencil stroke: Reference to the gp stroke inside Blender
    """

    # Init new stroke
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'  # allows for editing

    # Define stroke geometry
    gp_stroke.points.add(count=2)
    gp_stroke.points[0].co = p0
    apply_custom_vertex_config_leaves(gp_stroke.points[0])
    gp_stroke.points[0].pressure = thickness
    gp_stroke.points[1].co = p1
    apply_custom_vertex_config_leaves(gp_stroke.points[1])
    gp_stroke.points[1].pressure = thickness
    return gp_stroke


def draw_tree(tree=None, frame=0, overwrite=False, edit_gp_object=None):
    """
    For a given Space Colonization tree, go over all the branches and draw them with
    a brown material and different thickness.
    :param tree: Space Colonization tree object
    :param frame: Frame number
    :param bool overwrite: True if the edit_gp_object must be overwritten
                        False if a new gp_object must be created
    :param edit_gp_object: gp_object to overwrite (just used if overwrite=True)
    :return:
    grease pencil object: Reference to the gp object inside Blender
    """
    gp_material = create_material_color(material_name="Trunk", color=(0.0581109, 0.0284933, 0.0100318, 1), mode='LINE')

    if not overwrite:
        gp_object = get_gp_object(name="Tree_trunk", create_new=True)
    else:
        gp_object = edit_gp_object

    gp_layer = get_gp_layer(gp_object=gp_object, layer_name="Trunk", clear_layer=overwrite)

    gp_frame = get_frame_gp_layer(gp_layer=gp_layer, frame_number=frame)

    add_active_material_to_gp(gp_object=gp_object, material_to_add=gp_material)

    for branch in tree.branches:
        draw_line(gp_frame=gp_frame, p0=branch.pos, p1=branch.pos + branch.direction * branch.length, thickness=branch.thickness)

    return gp_object


def draw_leaves(tree=None, frame=0, overwrite=False, edit_gp_object=None):
    """
     For a given Space Colonization tree, go over all the leaves and draw them with
     a special leaf material and different thickness.
     :param tree: Space Colonization tree object
     :param frame: Frame number
     :param bool overwrite: True if the edit_gp_object must be overwritten
                            False if a new gp_object must be created
     :param edit_gp_object: gp_object to overwrite (just used if overwrite=True)
     :return:
     grease pencil object: Reference to the gp object inside Blender
     """

    # Add material with image
    # Get current addon path
    script_file = os.path.realpath(__file__)
    directory = os.path.dirname(script_file)
    img_dir = "{}/{}".format(directory, "leaves_texture.png")

    text_gp_img = import_image(image_path=img_dir)

    gp_material = create_material_texture(material_name="Leaves", color=(0.0, 0.0, 0.0, 1.0), mode='DOTS',
                                          text_img=text_gp_img)

    if not overwrite:
        gp_object = get_gp_object(name="Tree_leaves", create_new=True)
    else:
        gp_object = edit_gp_object

    gp_layer = get_gp_layer(gp_object=gp_object, layer_name="Leaves", clear_layer=overwrite)

    gp_frame = get_frame_gp_layer(gp_layer=gp_layer, frame_number=frame)

    add_active_material_to_gp(gp_object=gp_object, material_to_add=gp_material)

    # Create 2 points per leaf in order to draw a line
    for leaf in tree.original_leaves:
        p0 = leaf.pos + generate_random_direction() * 0.01
        p1 = leaf.pos + generate_random_direction() * 0.01

        draw_line_custom_leaves(gp_frame=gp_frame, p0=p0, p1=p1, thickness=random.uniform(200, 300))

    return gp_object


# PROPS

class GPT_property_group(bpy.types.PropertyGroup):
    collection_selector: bpy.props.PointerProperty(
        name="",
        description="GP Tree collection.",
        type=bpy.types.Collection
    )

    # EXAMPLE PROPERTY
    line_length: bpy.props.IntProperty(
        name="Length",
        description="Set the line length",
        min=1,
        max=500,
        default=50
    )


# OPERATORS

class GPT_OT_generate_tree(bpy.types.Operator):
    bl_idname = "gp_tree.generate_tree"
    bl_label = "Generate procedural tree"
    bl_description = "Generate procedural tree"

    @classmethod
    def poll(cls, context):
        if context.mode != 'OBJECT':
            return False
        return True

    def execute(self, context):
        try:
            # Execute the tree algorithm with the selected parameters
            my_tree = Tree(n_leaves=150, branch_length=0.02, influence_radius=0.7, kill_distance=0.02,
                           tree_crown_radius=0.7,
                           tree_crown_height=1.5, max_iterations=150, max_thickness=120)
            my_tree.generate_tree()

            gp_tree = draw_tree(tree=my_tree, frame=context.scene.frame_current, overwrite=False, edit_gp_object=None)
            gp_leaves = draw_leaves(tree=my_tree, frame=context.scene.frame_current, overwrite=False, edit_gp_object=None)

            # Create a new Blender collection and add the GP objects to it
            tree_collection = bpy.data.collections.new("GP_Tree")
            bpy.context.scene.collection.children.link(tree_collection)

            for collection in gp_tree.users_collection:
                collection.objects.unlink(gp_tree)

            for collection in gp_leaves.users_collection:
                collection.objects.unlink(gp_leaves)

            tree_collection.objects.link(gp_tree)
            tree_collection.objects.link(gp_leaves)

            context.scene.gp_tree.collection_selector = tree_collection


        except Exception as e:
            self.report({'ERROR'}, '{}'.format(e))
            return {"CANCELLED"}

        return {"FINISHED"}


class GPT_OT_overwrite_tree(bpy.types.Operator):
    bl_idname = "gp_tree.overwrite_tree"
    bl_label = "Overwrite current GP tree"
    bl_description = "Overwrite procedural tree"

    @classmethod
    def poll(cls, context):
        if context.mode != 'OBJECT':
            return False
        collection = context.scene.gp_tree.collection_selector
        if collection is None:
            return False
        if len(collection.all_objects) != 2:
            return False
        if not all('GPENCIL' in gp.type for gp in collection.all_objects):
            return False
        gp_leaves = [gp for gp in collection.all_objects if "Tree_leaves" in gp.name_full]
        gp_trunk = [gp for gp in collection.all_objects if "Tree_trunk" in gp.name_full]

        if len(gp_leaves) != 1:
            return False
        if len(gp_trunk) != 1:
            return False
        if "Leaves" not in gp_leaves[0].data.layers.keys():
            return False
        if "Trunk" not in gp_trunk[0].data.layers.keys():
            return False

        # If nothing is false, then true
        return True

    def execute(self, context):
        try:
            # Execute the tree algorithm with the selected parameters
            my_tree = Tree(n_leaves=150, branch_length=0.02, influence_radius=0.7, kill_distance=0.02,
                           tree_crown_radius=0.7,
                           tree_crown_height=1.5, max_iterations=150, max_thickness=120)
            my_tree.generate_tree()

            # Get gp object from current collection
            collection = context.scene.gp_tree.collection_selector
            gp_obj_trunk = [gp for gp in collection.all_objects if "Tree_trunk" in gp.name_full][0]
            gp_obj_leaves = [gp for gp in collection.all_objects if "Tree_leaves" in gp.name_full][0]

            gp_tree = draw_tree(tree=my_tree, frame=context.scene.frame_current, overwrite=True, edit_gp_object=gp_obj_trunk)
            gp_leaves = draw_leaves(tree=my_tree, frame=context.scene.frame_current, overwrite=True, edit_gp_object=gp_obj_leaves)


        except Exception as e:
            self.report({'ERROR'}, '{}'.format(e))
            return {"CANCELLED"}

        return {"FINISHED"}


# REGISTER

classes = [
    GPT_property_group,
    GPT_OT_generate_tree,
    GPT_OT_overwrite_tree
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.gp_tree = bpy.props.PointerProperty(
        name="Grease Pencil Tree",
        type=GPT_property_group,
        description="Information needed for generating a GP Tree"
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.types.Scene.gp_tree
