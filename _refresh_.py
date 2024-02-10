from importlib import reload
import sys
import bpy

from . import obake_normal
from . import obake_on_bake_complete

def reload_modules():
    if not bpy.context.preferences.view.show_developer_ui:
        return

    reload(sys.modules[__name__])
    reload(obake_normal)
    reload(obake_on_bake_complete)
