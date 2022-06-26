import bpy
from bpy.props import BoolProperty, FloatProperty, FloatVectorProperty, IntProperty


class CreateEye(bpy.types.Operator):
    """Create Eye"""

    bl_idname = "mesh.create_eye"
    bl_label = "Create Eye"
    bl_options = {"REGISTER", "UNDO"}

    glass_size: IntProperty(
        name="Glass Size",
        description="Glass Size",
        min=2,
        max=20,
        default=8,
    )

    pupil_size: FloatProperty(
        name="Pupil Size",
        description="Pupil Size",
        min=0.1,
        max=0.9,
        default=0.2,
    )

    iris_color1: FloatVectorProperty(
        name="color1",
        subtype="COLOR",
        default=(0, 0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        size=4,
        description="color picker",
    )

    iris_color2: FloatVectorProperty(
        name="color2",
        subtype="COLOR",
        default=(1.0, 0, 0, 1.0),
        min=0.0,
        max=1.0,
        size=4,
        description="color picker",
    )

    eye_ball_color: FloatVectorProperty(
        name="eye_ball",
        subtype="COLOR",
        default=(0.9, 0.8, 0.8, 1.0),
        min=0.0,
        max=1.0,
        size=4,
        description="color picker",
    )

    vein: BoolProperty(name="vein", description="Enable or Disable Vein", default=True)

    def execute(self, context):
        bpy.ops.mesh.eye_outside(
            glass_size=self.glass_size,
            vein=self.vein,
            eye_ball_color=self.eye_ball_color,
        )
        outside = bpy.context.view_layer.objects.active
        bpy.ops.mesh.eye_inside(
            pupil_size=self.pupil_size, color1=self.iris_color1, color2=self.iris_color2
        )
        inside = bpy.context.view_layer.objects.active
        bpy.ops.object.select_all(action="DESELECT")

        outside.select_set(True)
        inside.select_set(True)

        bpy.context.view_layer.objects.active = outside

        bpy.ops.object.parent_set()

        inside.select_set(False)

        obj = bpy.context.view_layer.objects.active
        obj["glass_size"] = self.glass_size
        obj["pupil_size"] = self.pupil_size
        obj["iris_color1"] = self.iris_color1
        obj["iris_color2"] = self.iris_color2
        obj["eye_ball_color"] = self.eye_ball_color
        obj["vein"] = self.vein

        return {"FINISHED"}


def register():
    bpy.utils.register_class(CreateEye)


def unregister():
    bpy.utils.unregister_class(CreateEye)


if __name__ == "__main__":
    register()
