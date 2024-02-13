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

bake_type_items = [
    ("normal", "Normal", ""),
    ("normalobj", "World space normal", ""),
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

    bake_type: bpy.props.EnumProperty(
        items=bake_type_items,
        default="normal",
        name="Bake Type"
    )

    selected_to_active: bpy.props.BoolProperty(
        name="Selected to Active",
        default=True,
        description="Bake Shading on the surface of selected objects to the active object"
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

    clear_image: bpy.props.BoolProperty(
        name="Clear Image",
        default=True,
        description="Clear Images before baking (internal only)"
    )

    margin_px: bpy.props.IntProperty(
        name="Margin",
        soft_min=0,
        soft_max=64,
        default=16,
        description="Extends the baked result as a post process filter"
    )

    def setup_image(self, name):
        px = 512
        if self.tex_size == "256":
            px = 256
        elif self.tex_size == "1k":
            px = 1024
        elif self.tex_size == "2k":
            px = 2048
        elif self.tex_size == "4k":
            px = 4096

        img_name = f"OBake_tex_AA{self.aa}_texset_{name}_{self.bake_type}_{px}"

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

        tex.name = "OBakeTargetImageTexture"
        tex.image = image
        nodes.active = tex

        links.new(tex_coord.outputs["UV"], mapping.inputs[0])
        links.new(mapping.outputs[0], tex.inputs[0])
        links.new(tex.outputs[0], normal_map.inputs[1])

        links.new(normal_map.outputs[0], bsdf.inputs["Normal"])
        links.new(bsdf.outputs[0], output_mat.inputs[0])

        return mat

    def set_target_texture(self, material, image):
        nodes = material.node_tree.nodes
        tex = nodes.get("OBakeTargetImageTexture") or nodes.new("ShaderNodeTexImage")

        tex.name = "OBakeTargetImageTexture"
        tex.image = image
        nodes.active = tex

    def bake_normal(self, context):
        coll = bpy.data.collections.get("OBake") or bpy.data.collections.new("OBake")
        coll.color_tag = "COLOR_06"
        if context.scene.collection.children.get("OBake") == None:
            context.scene.collection.children.link(coll)

        selected_objects = [obj for obj in context.selected_objects]
        dup_objects = set()
        active_dup_object = None
        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue
            copy_obj = bpy.data.objects.get("OBake_" + obj.name)
            if copy_obj == None:
                copy_obj = obj.copy()
                copy_obj.name = "OBake_" + obj.name
            if coll.objects.get(copy_obj.name) == None:
                coll.objects.link(copy_obj)
            dup_objects.add(copy_obj)
            if context.active_object == obj:
                active_dup_object = copy_obj

        for obj in selected_objects:
            obj.select_set(0)

        context.view_layer.objects.active = active_dup_object

        for obj in dup_objects:
            obj.select_set(1)
            for i, slot in enumerate(obj.material_slots):
                slot.link = "DATA"
                copy_mat = bpy.data.materials.get("OBake_mat_" + slot.material.name)
                if copy_mat == None:
                    copy_mat = slot.material.copy()
                    copy_mat.name = "OBake_mat_" + slot.material.name
                image = self.setup_image(slot.material.name)
                self.set_target_texture(copy_mat, image)
                obj.material_slots[i].link = "OBJECT"
                obj.material_slots[i].material = copy_mat

        margin_px = self.margin_px

        if self.aa == "x2":
            margin_px *= 2

        if self.bake_type == "normal":
            nrm_space = "TANGENT"
            nrm_R = "POS_X"
            nrm_G = "POS_Y"
            nrm_B = "POS_Z"
        else:
            nrm_space = "OBJECT"
            nrm_R = "POS_X"
            nrm_G = "POS_Z"
            nrm_B = "NEG_Y"

        bpy.ops.object.bake(
            "INVOKE_DEFAULT",
            type="NORMAL",
            normal_space=nrm_space,
            normal_r=nrm_R,
            normal_g=nrm_G,
            normal_b=nrm_B,
            use_clear=self.clear_image,
            use_selected_to_active=self.selected_to_active,
            cage_extrusion=self.extrusion,
            max_ray_distance=self.ray_distance,
            margin=margin_px
        )


    @classmethod
    def poll(cls, context):
        if context.scene.render.engine != "CYCLES":
            return False

        for obj in context.selected_objects:
            if obj.name.find("OBake_") >= 0:
                return False

        return context.active_object and context.active_object.type == "MESH"

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        self.bake_normal(context)

        return {"FINISHED"}
