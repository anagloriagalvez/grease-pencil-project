import bpy

# Import texture image to Blender
bpy.ops.image.open(filepath="C:\\Users\\Ana Gloria\\Desktop\\test.png")
gp_text_img = bpy.data.images['test.png'] # Arriesgado porque no sabemos el nombre

# Create material
gp_mat =  bpy.data.materials.new("My New Test Material")
bpy.data.materials.create_gpencil_data(gp_mat)
gp_mat.grease_pencil.color = (0.0, 0.0, 0.0, 1)
gp_mat.grease_pencil.show_stroke = True
gp_mat.grease_pencil.mode = 'DOTS'
gp_mat.grease_pencil.stroke_style = 'TEXTURE'
gp_mat.grease_pencil.stroke_image = gp_text_img
gp_mat.grease_pencil.mix_stroke_factor = 1.0
gp_mat.grease_pencil.alignment_mode = 'PATH'
gp_mat.grease_pencil.show_fill = False
