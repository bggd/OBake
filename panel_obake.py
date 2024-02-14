import bpy

class UI_PT_OBake(bpy.types.Panel):
    bl_idname = "UI_PT_OBake"
    bl_label = "OBake"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OBake"

    def draw(self, context):
        layout = self.layout

        layout.operator("obake.bake_normal")
