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

        # Adjust
        layout.label(text="Adjust Eye:")
        row = layout.row()
        adjust = row.operator("mesh.adjust_eye")

        obj = bpy.context.view_layer.objects.active

        glass_size = obj.get("glass_size")
        pupil_size = obj.get("pupil_size")
        iris_color1 = obj.get("iris_color1")
        iris_color2 = obj.get("iris_color2")
        eye_ball_color = obj.get("eye_ball_color")

        if glass_size and pupil_size and iris_color1 and iris_color2 and eye_ball_color:
            adjust.glass_size = glass_size
            adjust.pupil_size = pupil_size
            adjust.iris_color1 = iris_color1
            adjust.iris_color2 = iris_color2
            adjust.eye_ball_color = eye_ball_color


def register():
    bpy.utils.register_class(AizenPanel)


def unregister():
    bpy.utils.unregister_class(AizenPanel)


if __name__ == "__main__":
    register()
