from importlib import reload
import sys
import bpy

from . import obake_normal

def reload_modules():
    if not bpy.context.preferences.view.show_developer_ui:
        return

    reload(sys.modules[__name__])
    reload(obake_normal)
