import bpy
import pathlib

from .op_bake_normal import *

class OBJECT_OT_obake_export(bpy.types.Operator):
    bl_idname = "obake.export"
    bl_label = "Export"
    bl_options = {"REGISTER", "INTERNAL"}

    directory: bpy.props.StringProperty(
        name="Output Path",
        default="//",
        subtype="DIR_PATH",
        options={"HIDDEN"}
    )

    def export_images(self, context):
        dst_path =  pathlib.Path(bpy.path.abspath(self.directory))

        for i in bpy.data.images:
            if i.name.find("OBake_tex_") < 0:
                continue

            if len(i.pixels) == 0:
                continue

            file_path = dst_path / (i.name + ".png")
            i.save(filepath=str(file_path), quality=15)
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
