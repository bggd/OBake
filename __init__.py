bl_info = {
    "name": "OBake",
    "author": "birthggd",
    "description": "bake normalmap",
    "blender": (4, 0, 0),
    "version": (0, 0, 0),
    "location": "",
    "warning": "",
    "category": "Baking",
}

import bpy

from . import _refresh_

_refresh_.reload_modules()

classes = ()

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

