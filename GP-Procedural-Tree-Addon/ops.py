import bpy
from mathutils import *
from math import sin, cos, radians
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


def get_frame_gp_layer(gp_layer=None, frame_number=1):
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


def draw_tree_branch(gp_frame=None, p1=None, p2=None, n_points=50):
    gp_stroke = create_new_gp_stroke(gp_frame=gp_frame)
    gp_stroke.points.add(count=n_points+2)

    # Point1
    gp_point1 = gp_stroke.points[0]
    gp_point1.co = p1
    apply_custom_vertex_config_leaves(point=gp_point1)

    dir_vector = Vector(p2) - Vector(p1)
    line_length = dir_vector.magnitude
    point_dist = line_length / n_points

    for i in range(1, n_points+1):
        gp_point = gp_stroke.points[i]
        gp_point.co = Vector(p1) + dir_vector * point_dist * i
        apply_custom_vertex_config_leaves(point=gp_point)

    # Point2
    gp_point2 = gp_stroke.points[-1]
    gp_point2.co = p2
    apply_custom_vertex_config_leaves(point=gp_point2)

    return gp_stroke


def tree(x, y, angle, n_levels, branch_length, gp_frame):
    a = radians(angle)
    if n_levels:
        x1 = x + int(cos(a) * n_levels * branch_length)
        y1 = y + int(sin(a) * n_levels * branch_length)

        p1 = [x, y, 0]
        p2 = [x1, y1, 0]
        draw_tree_branch(gp_frame=gp_frame, p1=p1, p2=p2, n_points=50)

        # stroke = draw_shape(gp_frame, verts)
        # stroke.line_width = n_levels * 30

        # Right
        tree(x1, y1, angle, n_levels - 1, branch_length, gp_frame)

        # Left
        tree(x1, y1, -angle, n_levels - 1, branch_length, gp_frame)


# MAIN DRAWING METHOD
def draw_shape(gp_stroke=None, gp_frame=None):
    # draw_gp_line(gp_stroke=gp_stroke, n_points=bpy.context.scene.gp_tree.line_length)
    tree(x=0, y=0, angle=90, n_levels=5, branch_length=bpy.context.scene.gp_tree.line_length, gp_frame=gp_frame)


def apply_custom_vertex_config_leaves(point=None):
    point.vertex_color.data.vertex_color[0] = random.uniform(0.300, 0.350)  # Hue?
    point.vertex_color.data.vertex_color[1] = 0.502  # Saturation?
    point.vertex_color.data.vertex_color[2] = random.uniform(0.200, 0.300)  # Value?
    point.vertex_color.data.vertex_color[3] = random.uniform(0.0, 1.0)  # Alpha

    point.pressure = random.uniform(50, 500)
    point.uv_rotation = random.uniform(-1.0, 1.0)


def redraw_gp_tree(self, context):
    gp_name = context.scene.get("_current_gp_name")
    layer_name = context.scene.get("_current_gp_layer_name")

    if gp_name and layer_name:
        # TODO: Think more about this! Very risky as we don't know frame number, etc.
        gp_stroke = context.scene.objects[gp_name].data.layers[layer_name].frames[0].strokes[0]
        # remove_all_points_from_stroke(stroke=gp_stroke)
        gp_frame = context.scene.objects[gp_name].data.layers[layer_name].frames[0]
        gp_frame.clear()
        draw_shape(gp_stroke=gp_stroke, gp_frame=gp_frame)


def remove_all_points_from_stroke(stroke=None):
    points = stroke.points
    for i in range(0, len(points)):
        stroke.points.pop(index=0)


# PROPS

class GPT_property_group(bpy.types.PropertyGroup):
    line_length: bpy.props.IntProperty(
        name="Length",
        description="Set the line length",
        min=1,
        max=500,
        default=50,
        # TODO: FIX AS IT'S NOT WORKING
        update=redraw_gp_tree,  # Important for updating drawing
    )

    contactsheet_x: bpy.props.IntProperty(
        name="Resolution X",
        default=1920,
        min=100,
        description="X resolution of contactsheet",
    )
    contactsheet_y: bpy.props.IntProperty(
        name="Resolution Y",
        default=1080,
        min=100,
        description="Y resolution of contactsheet",
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
            # Add material with image
            text_gp_img = import_image(
                image_path="d:\\agalvez\\Desktop\\grease-pencil-project-main\\test.png")
            gp_material = create_material_texture(text_img=text_gp_img)

            gp_object = get_gp_object()

            gp_layer = get_gp_layer(gp_object=gp_object, layer_name="Test layer")

            # Important! Otherwise, thickness = 0
            change_gp_layer_line_thickness(gp_layer=gp_layer, thickness=100)

            gp_frame = get_frame_gp_layer(gp_layer=gp_layer, frame_number=context.scene.frame_current)

            gp_stroke = create_new_gp_stroke(gp_frame=gp_frame)

            # Add desired material to stroke
            add_active_material_to_gp(gp_object=gp_object, material_to_add=gp_material)

            # Experimental! Add stroke to custom properties on scene
            context.scene["_current_gp_name"] = gp_object.name_full
            context.scene["_current_gp_layer_name"] = gp_layer.info  # Layer name
            # context.scene["_current_gp_frame"] = bpy.context.scene.frame_current

            draw_shape(gp_stroke=gp_stroke, gp_frame=gp_frame)

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
