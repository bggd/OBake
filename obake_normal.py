import bpy

texture_size_items = [
    ("256", "256 x 256", ""),
    ("512", "512 x 512", ""),
    ("1k", "1024 x 1024", ""),
    ("2k", "2048 x 2048", ""),
    ("4k", "4096 x 4096", ""),
]


class OBake_OT_bake_normal(bpy.types.Operator):
    bl_idname = "obake.bake_normal"
    bl_label = "Bake Normal map"

    tex_size: bpy.props.EnumProperty(items=texture_size_items, default="512", name="Texture Size")

    def setup_material(self, context):
        mat_name = "OBake_mat"
        mat = bpy.data.materials.get(mat_name) or bpy.data.materials.new(mat_name)
        mat.use_nodes = True

        node_tree = mat.node_tree

        tex_name = "OBake_tex"
        tex = node_tree.nodes.get(tex_name) or node_tree.nodes.new("ShaderNodeTexImage")
        tex.name = tex_name

        px = 512
        if self.tex_size == "256":
            px = 256
        elif self.tex_size == "1k":
            px = 1024
        elif self.tex_size == "2k":
            px = 2048
        elif self.tex_size == "4k":
            px = 4096

        img_name = f"OBake_tex_{px}"
        img = bpy.data.images.get(img_name) or bpy.data.images.new(img_name, px, px, float_buffer=True, is_data=True)

        tex.image = img
        node_tree.nodes.active = tex

        return mat

    def bake_normal(self, context):
        mat = self.setup_material(context)

        obj = context.active_object
        obj.active_material = mat

        bpy.ops.object.bake(
            "INVOKE_DEFAULT",
            type="NORMAL",
            use_clear=True,
            use_selected_to_active=True
        )

    @classmethod
    def poll(cls, context):
        return context.object.type == "MESH"

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        self.bake_normal(context)

        return {"FINISHED"}
