import bpy


class GPT_PT_mainPanel(bpy.types.Panel):
    bl_label = "Grease Pencil Procedural Tree"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Grease Pencil Tree"

    def draw(self, context):
        layout = self.layout
        # layout.use_property_split = True
        box = layout.box()
        row = box.row(align=True)
        row.label(text='Generate tree')

        row = box.row(align=True)
        row.scale_y = 1.4
        row.operator('gp_tree.overwrite_tree', text='Edit current', icon='GREASEPENCIL')
        # row.separator_spacer()
        row.prop(context.scene.gp_tree, "collection_selector")

        row = box.row(align=True)
        row.scale_y = 1.4
        row.operator('gp_tree.generate_tree', text='New tree', icon='OUTLINER_DATA_GP_LAYER')


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
