import bpy
from bpy.props import BoolProperty, FloatProperty, FloatVectorProperty, IntProperty


class AdjustEye(bpy.types.Operator):
    """Adjust Eye"""

    bl_idname = "mesh.adjust_eye"
    bl_label = "Adjust Eye"
    bl_options = {"REGISTER", "UNDO"}

    glass_size: IntProperty(
        name="Glass Size",
        description="Glass Size",
        min=0,
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
        default=(1.0, 1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        size=4,
        description="color picker",
    )

    iris_color2: FloatVectorProperty(
        name="color2",
        subtype="COLOR",
        default=(1.0, 1.0, 1.0, 1.0),
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

    def execute(self, context):
        outside = bpy.context.view_layer.objects.active
        location = outside.location.copy()
        rotation_euler = outside.rotation_euler.copy()
        scale = outside.scale.copy()
        bpy.ops.object.select_hierarchy(direction="CHILD", extend=False)
        inside = bpy.context.view_layer.objects.active
        bpy.data.objects.remove(outside)
        bpy.data.objects.remove(inside)

        bpy.ops.mesh.create_eye(
            glass_size=self.glass_size,
            pupil_size=self.pupil_size,
            iris_color1=self.iris_color1,
            iris_color2=self.iris_color2,
            eye_ball_color=self.eye_ball_color,
        )

        target = bpy.context.view_layer.objects.active

        target.location = location
        target.rotation_euler = rotation_euler
        target.scale = scale

        obj = bpy.context.view_layer.objects.active
        obj["glass_size"] = self.glass_size
        obj["pupil_size"] = self.pupil_size
        obj["iris_color1"] = self.iris_color1
        obj["iris_color2"] = self.iris_color2
        obj["eye_ball_color"] = self.eye_ball_color

        return {"FINISHED"}


def register():
    bpy.utils.register_class(AdjustEye)


def unregister():
    bpy.utils.unregister_class(AdjustEye)


if __name__ == "__main__":
    register()
