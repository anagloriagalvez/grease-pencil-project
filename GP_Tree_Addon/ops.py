import bpy
from mathutils import *
from .SC_Algorithm.tree import Tree
import random


# FUNCTIONS


def import_image(image_path=None):
    # Import texture image to Blender
    image = bpy.data.images.load(filepath=image_path)

    return image


def create_material_texture(material_name="New Test Material", color=(0.0, 0.0, 0.0, 1.0), mode='DOTS', text_img=None):
    # Create material
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


def create_material_color(material_name="New Test Material", color=(0.133615, 0.0622937, 0.0196455, 1), mode='LINE'):
    # Create material
    gp_mat = bpy.data.materials.new(material_name)
    bpy.data.materials.create_gpencil_data(gp_mat)
    gp_mat.grease_pencil.color = color
    gp_mat.grease_pencil.show_stroke = True
    gp_mat.grease_pencil.mode = mode
    gp_mat.grease_pencil.stroke_style = 'SOLID'
    gp_mat.grease_pencil.mix_stroke_factor = 1.0
    gp_mat.grease_pencil.show_fill = False
    print("CREATING MATERIAL")

    return gp_mat


def get_gp_material(name="New Test Material"):
    gp_material = bpy.data.materials[name]
    return gp_material


def get_gp_object(name='GPencil', create_new=True):
    # If not in scene, add a new object
    if name not in bpy.context.scene.objects or create_new:
        bpy.ops.object.gpencil_add(type="EMPTY")
        # Change name
        bpy.context.selected_objects[0].name = name
    return bpy.context.scene.objects[name]


def get_gp_layer(gp_object=None, layer_name="My layer"):
    # if clear_layer:
    #     gpencil_layer.clear()
    if layer_name in gp_object.data.layers.keys():  # List of layer names
        return gp_object.data.layers[layer_name]
    return gp_object.data.layers.new(name=layer_name, set_active=True)


def change_gp_layer_line_thickness(gp_layer=None, thickness=1):
    gp_layer.line_change = thickness


def get_frame_gp_layer(gp_layer=None, frame_number=0):
    for index, frame in enumerate(gp_layer.frames):
        if frame.frame_number == frame_number:
            return gp_layer.frames[index]
    # If not found, or we want to override it, return new frame
    return gp_layer.frames.new(frame_number)


def create_new_gp_stroke(gp_frame=None):
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'  # allows for editing
    return gp_stroke


def add_active_material_to_gp(gp_object=None, material_to_add=None):
    gp_object.data.materials.append(material_to_add)
    gp_object.active_material = material_to_add


# TODO: Think much more on that
def draw_gp_line(gp_stroke=None, n_points=50):
    # Define stroke geometry
    gp_stroke.points.add(count=n_points)

    # Draw a 50points line with a random (but controlled) color value
    for i in range(0, n_points):
        gp_point = gp_stroke.points[i]
        gp_point.co = Vector((0.0, 0.0, float(i / 32)))

        apply_custom_vertex_config_leaves(point=gp_point)


# MAIN DRAWING METHOD
def apply_custom_vertex_config_leaves(point=None):
    point.vertex_color.data.vertex_color[0] = random.uniform(0.300, 0.350)  # Hue?
    point.vertex_color.data.vertex_color[1] = 0.502  # Saturation?
    point.vertex_color.data.vertex_color[2] = random.uniform(0.200, 0.300)  # Value?
    point.vertex_color.data.vertex_color[3] = random.uniform(0.0, 1.0)  # Alpha

    # point.pressure = random.uniform(50, 500)
    # point.uv_rotation = random.uniform(-1.0, 1.0)


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


def draw_tree(tree, context):
    gp_material = create_material_color()

    gp_object = get_gp_object()

    gp_layer = get_gp_layer(gp_object=gp_object, layer_name="Test layer")

    gp_frame = get_frame_gp_layer(gp_layer=gp_layer, frame_number=context.scene.frame_current)

    add_active_material_to_gp(gp_object=gp_object, material_to_add=gp_material)

    for branch in tree.branches:
        draw_line(gp_frame, branch.pos, branch.pos + branch.direction * branch.length, branch.thickness)


def draw_leaves(tree):
    for leaf in tree.original_leaves:
        bpy.ops.mesh.primitive_uv_sphere_add(location=leaf.pos, radius=0.025)


# PROPS

class GPT_property_group(bpy.types.PropertyGroup):
    line_length: bpy.props.IntProperty(
        name="Length",
        description="Set the line length",
        min=1,
        max=500,
        default=50
    )

    # EXAMPLE PROPERTY
    contactsheet_x: bpy.props.IntProperty(
        name="Resolution X",
        default=1920,
        min=100,
        description="X resolution of contactsheet",
    )


# OPERATORS

class GPT_OT_generate_tree(bpy.types.Operator):
    bl_idname = "gp_tree.generate_tree"
    bl_label = "Generate procedural tree"
    bl_description = "Generate procedural tree"

    # @classmethod
    # def poll(cls, context):
    #     return True

    def execute(self, context):
        try:
            # Execute the tree algorithm with the selected parameters
            my_tree = Tree(n_leaves=150, branch_length=0.02, influence_radius=0.7, kill_distance=0.02,
                           tree_crown_radius=1,
                           tree_crown_height=1.5, max_iterations=150, max_thickness=80)
            my_tree.generate_tree()

            # Add material with image
            # text_gp_img = import_image(
            #     image_path="{}/leaves_texture.png".format(os.getcwd()))
            # gp_material = create_material_texture(text_img=text_gp_img)

            gp_object = get_gp_object()

            gp_layer = get_gp_layer(gp_object=gp_object, layer_name="Test layer")

            # Important! Otherwise, thickness = 0
            # change_gp_layer_line_thickness(gp_layer=gp_layer, thickness=100)

            gp_frame = get_frame_gp_layer(gp_layer=gp_layer, frame_number=context.scene.frame_current)

            gp_stroke = create_new_gp_stroke(gp_frame=gp_frame)

            # Add desired material to stroke
            # add_active_material_to_gp(gp_object=gp_object, material_to_add=gp_material)

            # Experimental! Add stroke to custom properties on scene
            context.scene["_current_gp_name"] = gp_object.name_full
            context.scene["_current_gp_layer_name"] = gp_layer.info  # Layer name
            # context.scene["_current_gp_material_name"] = gp_material.name_full  # Material name
            # context.scene["_current_gp_frame"] = bpy.context.scene.frame_current

            draw_tree(my_tree, context)
            draw_leaves(my_tree)

        except Exception as e:
            self.report({'ERROR'}, '{}'.format(e))
            return {"CANCELLED"}

        return {"FINISHED"}


# REGISTER

classes = [
    GPT_property_group,
    GPT_OT_generate_tree
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
