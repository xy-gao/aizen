import bpy
from bpy.props import EnumProperty


class MirrorEye(bpy.types.Operator):
    """Mirror Eye"""

    bl_idname = "mesh.mirror_eye"
    bl_label = "Mirror Eye"
    bl_options = {"REGISTER", "UNDO"}

    mirror: EnumProperty(
        items=[("X", "X", "X"), ("Y", "Y", "Y"), ("Z", "Z", "Z")],
        name="mirror axis",
        description="Enable or Disable mirror",
        default="X",
    )

    def execute(self, context):
        bpy.ops.object.select_hierarchy(direction="CHILD", extend=True)
        bpy.ops.object.duplicate()
        bpy.ops.view3d.snap_cursor_to_center()
        prev_pivot_point = bpy.context.scene.tool_settings.transform_pivot_point
        bpy.context.scene.tool_settings.transform_pivot_point = "CURSOR"

        if self.mirror == "X":
            bpy.ops.transform.mirror(
                orient_type="GLOBAL",
                orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                orient_matrix_type="GLOBAL",
                constraint_axis=(True, False, False),
            )

        if self.mirror == "Y":
            bpy.ops.transform.mirror(
                orient_type="GLOBAL",
                orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                orient_matrix_type="GLOBAL",
                constraint_axis=(False, True, False),
            )
        if self.mirror == "Z":
            bpy.ops.transform.mirror(
                orient_type="GLOBAL",
                orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                orient_matrix_type="GLOBAL",
                constraint_axis=(False, False, True),
            )

        bpy.ops.object.select_hierarchy(direction="PARENT", extend=False)

        bpy.context.scene.tool_settings.transform_pivot_point = prev_pivot_point
        return {"FINISHED"}


def register():
    bpy.utils.register_class(MirrorEye)


def unregister():
    bpy.utils.unregister_class(MirrorEye)


if __name__ == "__main__":
    register()
