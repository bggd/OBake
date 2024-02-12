import bpy

texture_size_items = [
    ("256", "256 x 256", ""),
    ("512", "512 x 512", ""),
    ("1k", "1024 x 1024", ""),
    ("2k", "2048 x 2048", ""),
    ("4k", "4096 x 4096", ""),
]

aa_items = [
    ("None", "None", ""),
    ("x2", "Subsampling 2x2", ""),
]


class OBake_OT_bake_normal(bpy.types.Operator):
    bl_idname = "obake.bake_normal"
    bl_label = "Bake Normal map"

    tex_size: bpy.props.EnumProperty(
        items=texture_size_items,
        default="512",
        name="Texture Size"
    )

    aa: bpy.props.EnumProperty(
        items=aa_items,
        default="None",
        name="Antialiasing"
    )

    extrusion: bpy.props.FloatProperty(
        name="Extrusion",
        soft_min=0.0,
        soft_max=1.0,
        precision=3,
        step=1,
        description="Inflate the active object by the specified distance for baking. This helps matching to points nearer to the outside of the selected object meshes"
    )

    ray_distance: bpy.props.FloatProperty(
        name="Max Ray Distance",
        soft_min=0.0,
        soft_max=1.0,
        precision=3,
        step=1,
        description="The maximum ray distance for matching points between the active and selected objects. If zero, there is no limit",
    )

    margin_px: bpy.props.IntProperty(
        name="Margin",
        soft_min=0,
        soft_max=64,
        default=16,
        description="Extends the baked result as a post process filter"
    )

    def setup_image(self, context):
        px = 512
        if self.tex_size == "256":
            px = 256
        elif self.tex_size == "1k":
            px = 1024
        elif self.tex_size == "2k":
            px = 2048
        elif self.tex_size == "4k":
            px = 4096

        img_name = f"OBake_tex_AA{self.aa}_{px}"

        if self.aa == "x2":
            px *= 2

        img = bpy.data.images.get(img_name) or bpy.data.images.new(img_name, px, px, float_buffer=True, is_data=True)

        if self.aa == "x2":
            img.scale(px, px)

        return img


    def setup_material(self, context, image):
        mat_name = "OBake_mat"
        mat = bpy.data.materials.get(mat_name) or bpy.data.materials.new(mat_name)
        mat.use_nodes = True

        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        nodes.clear()

        output_mat = nodes.new("ShaderNodeOutputMaterial")
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")

        tex_coord = nodes.new("ShaderNodeTexCoord")
        mapping = nodes.new("ShaderNodeMapping")
        tex = nodes.new("ShaderNodeTexImage")
        normal_map = nodes.new("ShaderNodeNormalMap")

        offset_x = 0
        for i in [tex_coord, mapping, tex, normal_map, bsdf, output_mat]:
            i.location.x = offset_x
            offset_x += 300

        tex.image = image
        nodes.active = tex

        links.new(tex_coord.outputs["UV"], mapping.inputs[0])
        links.new(mapping.outputs[0], tex.inputs[0])
        links.new(tex.outputs[0], normal_map.inputs[1])

        links.new(normal_map.outputs[0], bsdf.inputs["Normal"])
        links.new(bsdf.outputs[0], output_mat.inputs[0])

        return mat

    def bake_normal(self, context):
        img = self.setup_image(context)
        mat = self.setup_material(context, img)

        obj = context.active_object
        obj.active_material = mat

        margin_px = self.margin_px

        if self.aa == "x2":
            margin_px *= 2

        bpy.ops.object.bake(
            "INVOKE_DEFAULT",
            type="NORMAL",
            use_clear=True,
            use_selected_to_active=True,
            cage_extrusion=self.extrusion,
            max_ray_distance=self.ray_distance,
            margin=margin_px
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
