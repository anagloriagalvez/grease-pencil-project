import bpy
from mathutils import *
from math import *
import random

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

def create_new_gp_object():
    bpy.ops.object.gpencil_add(type="EMPTY")
    return bpy.context.selected_objects[0]

def create_new_gp_layer(gp_object=None, layer_name="My layer"):
    return gp_object.data.layers.new(name=layer_name, set_active=True)

def change_gp_layer_line_thickness(gp_layer=None, thickness=1):
    gp_layer.line_change = 100

def create_new_frame_gp_layer(gp_layer=None, frame_number=0):
    return gp_layer.frames.new(frame_number)

def create_new_gp_stroke(gp_frame=None):
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'  # allows for editing
    return gp_stroke

def add_active_material_to_gp(gp_object=None, material_to_add=None):
    gp_object.data.materials.append(material_to_add)
    gp_object.active_material = material_to_add

# TODO: Think much more on that
def draw_gp_line(gp_stroke=None):
    # Define stroke geometry
    n_points = 50
    gp_stroke.points.add(count=50)

    # Draw a 50points line with a random (but controlled) color value
    for i in range(0, 50):
        gp_point = gp_stroke.points[i]
        gp_point.co = Vector((0.0, 0.0, float(i / 32)))

        apply_custom_vertex_config_leaves(point=gp_point)

def apply_custom_vertex_config_leaves(point=None):
    point.vertex_color.data.vertex_color[0] = random.uniform(0.300, 0.350)  # Hue?
    point.vertex_color.data.vertex_color[1] = 0.502  # Saturation?
    point.vertex_color.data.vertex_color[2] = random.uniform(0.200, 0.300)  # Value?
    point.vertex_color.data.vertex_color[3] = random.uniform(0.0, 1.0)  # Alpha

    point.pressure = random.uniform(50, 500)
    point.uv_rotation = random.uniform(-1.0, 1.0)


if __name__ == "__main__":

    # Add material with image
    text_gp_img = import_image(image_path="C:\\Users\\Ana Gloria\\Desktop\\TFG\\grease-pencil-project\\test.png")
    gp_material = create_material_texture(text_img=text_gp_img)

    gp_object = create_new_gp_object()
    gp_object_name = gp_object.name_full

    gp_layer = create_new_gp_layer(gp_object=gp_object, layer_name="Test layer")

    # Important! Otherwise, thickness = 0
    change_gp_layer_line_thickness(gp_layer=gp_layer, thickness=10)

    gp_frame = create_new_frame_gp_layer(gp_layer=gp_layer, frame_number=1)

    gp_stroke = create_new_gp_stroke(gp_frame=gp_frame)

    # Add desired material to stroke
    add_active_material_to_gp(gp_object=gp_object, material_to_add=gp_material)

    draw_gp_line(gp_stroke=gp_stroke)
