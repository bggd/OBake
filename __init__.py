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

from .obake_normal import *
from .obake_on_bake_complete import *

from .panel_obake import *

classes = (OBake_OT_bake_normal, UI_PT_OBake)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.app.handlers.object_bake_complete.append(on_bake_complete)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.app.handlers.object_bake_complete.remove(on_bake_complete)

if __name__ == "__main__":
    register()

