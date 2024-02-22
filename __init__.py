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

from .op_bake_normal import *
from .op_export import *
from .obake_on_bake_complete import *

from .prop_export import *

from .panel_obake import *
from .panel_export import *

classes = (
    OBJECT_OT_obake_bake_normal,
    OBJECT_OT_obake_export,
    ExpoprtSettings,
    UI_PT_OBake,
    UI_PT_OBake_Export
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.obake_export_settings = bpy.props.PointerProperty(type=ExpoprtSettings)

    bpy.app.handlers.object_bake_complete.append(on_bake_complete)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.WindowManager.obake_export_settings

    bpy.app.handlers.object_bake_complete.remove(on_bake_complete)

if __name__ == "__main__":
    register()

