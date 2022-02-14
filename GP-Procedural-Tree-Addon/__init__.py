bl_info = {
"name": "Grease Pencil Procedural Tree",
"description": "Generate Grease Pencil trees and modify them procedurally",
"author": "Ana Gloria Gálvez Mellado",
"version": (0, 0, 1),
"blender": (3, 0, 0),
"location": "Sidebar > Grease Pencil > Grease Pencil Tree",
"warning": "",
"category": "Object",
}

from .  import (
                ops,
                ui_panels,
                )

def register():
    ops.register()
    ui_panels.register()

def unregister():
    ui_panels.unregister()
    ops.unregister()

if __name__ == "__main__":
    register()
