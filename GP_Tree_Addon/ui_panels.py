import bpy


class GPT_PT_mainPanel(bpy.types.Panel):
    bl_label = "Grease Pencil Procedural Tree"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Grease Pencil Tree"

    def draw(self, context):
        layout = self.layout
        # layout.use_property_split = True

        # row = layout.row(align=True)
        # row.prop(context.scene.gp_tree, "line_length", text="Line length")

        row = layout.row(align=True)
        row.operator('gp_tree.generate_tree', text='Generate tree', icon='OUTLINER_DATA_GP_LAYER')


# REGISTER

classes = [
    GPT_PT_mainPanel,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
