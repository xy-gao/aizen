import bpy


class AizenPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""

    bl_label = "Eye Generator"
    bl_idname = "OBJECT_PT_AIZEN"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Aizen"

    def draw(self, context):
        layout = self.layout

        # Create Eye
        layout.label(text="Create Eye:")
        row = layout.row()
        row.operator("mesh.create_eye")


def register():
    bpy.utils.register_class(AizenPanel)


def unregister():
    bpy.utils.unregister_class(AizenPanel)


if __name__ == "__main__":
    register()
