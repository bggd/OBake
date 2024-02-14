import bpy

class UI_PT_OBake_Export(bpy.types.Panel):
    bl_idname = "UI_PT_OBake_Export"
    bl_label = "Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OBake"

    def draw(self, context):
        layout = self.layout
