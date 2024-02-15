import bpy

@bpy.app.handlers.persistent
def on_bake_complete(dummy):
    for i in bpy.data.images:
        if i.name.find("OBake_tex_AAx2_") < 0:
            continue
        size = int(i.name.split("_")[3])
        i.scale(size, size)
