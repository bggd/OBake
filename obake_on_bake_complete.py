import bpy

@bpy.app.handlers.persistent
def on_bake_complete(dummy):
    for i in bpy.data.images:
        if i.name.find("OBake_tex_AAx2_") < 0:
            continue
        size = int(i.name.split("_")[-1])
        i.scale(size, size)

    for i in bpy.data.materials:
        if i.name == "OBake_mat":
            continue
        if i.node_tree and i.node_tree.nodes:
            nodes = i.node_tree.nodes
            n = nodes.get("OBakeTargetImageTexture")
            if n:
                nodes.remove(n)
