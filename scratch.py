import bpy
from mathutils import *
from math import *
import random

gp_layer = bpy.data.objects['Test'].data.layers.new(name="testlayer", set_active=True)
gp_layer.line_change = 100  # Important! Otherwise, thickness = 0

gp_frame = gp_layer.frames.new(0)

gp_stroke = gp_frame.strokes.new()
gp_stroke.display_mode = '3DSPACE'  # allows for editing

# Define stroke geometry
n_points = 50
gp_stroke.points.add(count=50)

# Draw a 50points line with a random (but controlled) color value
for i in range(0, 50):
    gp_stroke.points[i].co = Vector((0.0, 0.0, float(i / 32)))

    gp_stroke.points[i].vertex_color.data.vertex_color[0] = 0.2
    gp_stroke.points[i].vertex_color.data.vertex_color[1] = 0.4
    gp_stroke.points[i].vertex_color.data.vertex_color[2] = 1.0
    gp_stroke.points[i].vertex_color.data.vertex_color[3] = 1.0  # Alpha

    gp_stroke.points[i].vertex_color.data.vertex_color[0] = random.uniform(0.300, 0.350)  # Hue?
    gp_stroke.points[i].vertex_color.data.vertex_color[1] = 0.502  # Saturation?
    gp_stroke.points[i].vertex_color.data.vertex_color[2] = random.uniform(0.200, 0.300)  # Value?
    gp_stroke.points[i].vertex_color.data.vertex_color[3] = random.uniform(0.0, 1.0)  # Alpha

    gp_stroke.points[i].pressure = random.uniform(50, 255)
    gp_stroke.points[i].uv_rotation = random.uniform(-1.0, 1.0)
