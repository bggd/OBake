import bpy

from .op_bake_normal import *

class OBJECT_OT_export(bpy.types.Operator):
    bl_idname = "obake.export"
    bl_label = "Export"
    bl_options = {"REGISTER", "PRESET"}

    output_path: bpy.props.StringProperty(
        name="Output Path",
        default="//",
        subtype="DIR_PATH"
    )

    def export_images(self, context):
        dst_path = bpy.path.abspath(self.output_path)

        for i in bpy.data.images:
            if i.name.find("OBake_tex_") < 0:
                continue

            file_path = dst_path + i.name + ".png"
            i.save(filepath=file_path, quality=15)
            self.report({"INFO"}, f"{file_path} is saved!")

    @classmethod
    def poll(cls, context):
        return bpy.path.abspath("//") != ""

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        self.export_images(context)

        return {"FINISHED"}
