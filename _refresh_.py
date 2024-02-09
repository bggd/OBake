from importlib import reload
import sys
import bpy

def reload_modules():
    if not bpy.context.preferences.view.show_developer_ui:
        return
