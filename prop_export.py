import bpy

class ExpoprtSettings(bpy.types.PropertyGroup):
    output_path: bpy.props.StringProperty(
        name="Output Path",
        default="//",
        subtype="DIR_PATH",
    )
