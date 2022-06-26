import bpy
from bpy.props import FloatProperty, FloatVectorProperty


def add_inside(pupil_size):
    bpy.ops.mesh.primitive_circle_add(
        enter_editmode=False, align="WORLD", location=(0, 0, 0), scale=(1, 1, 1)
    )

    bpy.ops.transform.rotate(
        value=1.5708,
        orient_axis="X",
        orient_type="GLOBAL",
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        orient_matrix_type="GLOBAL",
        constraint_axis=(True, False, False),
        mirror=True,
        use_proportional_edit=False,
        proportional_edit_falloff="SMOOTH",
        proportional_size=1,
        use_proportional_connected=False,
        use_proportional_projected=False,
    )

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.edge_face_add()

    bpy.ops.mesh.inset(thickness=1 - pupil_size, depth=0, release_confirm=True)
    bpy.ops.transform.translate(
        value=(0, 0.2, 0),
        orient_type="GLOBAL",
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        orient_matrix_type="GLOBAL",
        constraint_axis=(True, True, True),
        mirror=True,
        use_proportional_edit=False,
        proportional_edit_falloff="SMOOTH",
        proportional_size=1,
        use_proportional_connected=False,
        use_proportional_projected=False,
    )

    bpy.ops.mesh.extrude_region_move(
        MESH_OT_extrude_region={
            "use_normal_flip": False,
            "use_dissolve_ortho_edges": False,
            "mirror": False,
        },
        TRANSFORM_OT_translate={
            "value": (0, 0.5, 0),
            "orient_type": "GLOBAL",
            "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            "orient_matrix_type": "GLOBAL",
            "constraint_axis": (False, True, False),
            "mirror": False,
            "use_proportional_edit": False,
            "proportional_edit_falloff": "SMOOTH",
            "proportional_size": 1,
            "use_proportional_connected": False,
            "use_proportional_projected": False,
            "snap": False,
            "snap_target": "CLOSEST",
            "snap_point": (0, 0, 0),
            "snap_align": False,
            "snap_normal": (0, 0, 0),
            "gpencil_strokes": False,
            "cursor_transform": False,
            "texture_space": False,
            "remove_on_cancel": False,
            "release_confirm": False,
            "use_accurate": False,
            "use_automerge_and_split": False,
        },
    )

    bpy.ops.object.modifier_add(type="BEVEL")

    bpy.context.object.modifiers["Bevel"].width = 0.03
    bpy.context.object.modifiers["Bevel"].segments = 3

    bpy.ops.object.editmode_toggle()
    bpy.ops.object.modifier_apply(modifier="Bevel")

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.region_to_loop()
    bpy.ops.mesh.extrude_region_move(
        MESH_OT_extrude_region={
            "use_normal_flip": False,
            "use_dissolve_ortho_edges": False,
            "mirror": False,
        },
        TRANSFORM_OT_translate={
            "value": (0, 0.5, 0),
            "orient_axis_ortho": "X",
            "orient_type": "GLOBAL",
            "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            "orient_matrix_type": "GLOBAL",
            "constraint_axis": (False, True, False),
            "mirror": False,
            "use_proportional_edit": False,
            "proportional_edit_falloff": "SMOOTH",
            "proportional_size": 1,
            "use_proportional_connected": False,
            "use_proportional_projected": False,
            "snap": False,
            "snap_target": "CLOSEST",
            "snap_point": (0, 0, 0),
            "snap_align": False,
            "snap_normal": (0, 0, 0),
            "gpencil_strokes": False,
            "cursor_transform": False,
            "texture_space": False,
            "remove_on_cancel": False,
            "view2d_edge_pan": False,
            "release_confirm": False,
            "use_accurate": False,
            "use_automerge_and_split": False,
        },
    )
    bpy.ops.transform.resize(
        value=(1.12, 1.12, 1.12),
        orient_type="GLOBAL",
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        orient_matrix_type="GLOBAL",
        mirror=True,
        use_proportional_edit=False,
        proportional_edit_falloff="SMOOTH",
        proportional_size=1,
        use_proportional_connected=False,
        use_proportional_projected=False,
    )
    bpy.ops.object.editmode_toggle()

    bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)

    import math

    def circle_func(x):
        return math.sqrt(1 - x**2)

    scale_size = circle_func(bpy.context.scene.cursor.location[1]) - 0.01

    bpy.ops.transform.resize(
        value=(scale_size, scale_size, scale_size),
        orient_type="GLOBAL",
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        orient_matrix_type="GLOBAL",
        mirror=False,
        use_proportional_edit=False,
        proportional_edit_falloff="SMOOTH",
        proportional_size=1,
        use_proportional_connected=False,
        use_proportional_projected=False,
    )

    bpy.ops.transform.translate(
        value=(0, 0.05, 0),
        orient_axis_ortho="X",
        orient_type="GLOBAL",
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        orient_matrix_type="GLOBAL",
        constraint_axis=(False, True, False),
        mirror=False,
        use_proportional_edit=False,
        proportional_edit_falloff="SMOOTH",
        proportional_size=1,
        use_proportional_connected=False,
        use_proportional_projected=False,
    )

    bpy.ops.object.shade_smooth()
    bpy.ops.view3d.snap_cursor_to_center()


def eye_inside_material(pupil_size, color1, color2):
    mat = bpy.data.materials.new(name="Eye Inside")
    mat.use_nodes = True
    mat.shadow_method = "NONE"
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    texcoord_node = nodes.new("ShaderNodeTexCoord")
    texcoord_node.location = (-1200, 100)

    mapping_iris_node = nodes.new("ShaderNodeMapping")
    mapping_iris_node.location = (-1000, 100)
    mapping_iris_node.vector_type = "NORMAL"
    mapping_iris_node.inputs["Scale"].default_value[2] = 2

    mapping_pupil_node = nodes.new("ShaderNodeMapping")
    mapping_pupil_node.location = (-1000, 500)
    mapping_pupil_node.inputs["Scale"].default_value[2] = 0

    noise_node = nodes.new("ShaderNodeTexNoise")
    noise_node.location = (-800, 100)
    noise_node.inputs["Detail"].default_value = 3

    gradient_node = nodes.new("ShaderNodeTexGradient")
    gradient_node.location = (-800, 300)
    gradient_node.gradient_type = "SPHERICAL"

    iris_color_ramp_node = nodes.new("ShaderNodeValToRGB")
    iris_color_ramp_node.location = (-600, 100)
    iris_color_ramp_node.color_ramp.elements[0].position = 0.18

    pupil_color_ramp_node = nodes.new("ShaderNodeValToRGB")
    pupil_color_ramp_node.location = (-600, 400)
    pupil_color_ramp_node.color_ramp.elements[0].position = 0.9 - pupil_size
    pupil_color_ramp_node.color_ramp.elements[0].color = (1, 1, 1, 1)

    pupil_color_ramp_node.color_ramp.elements[1].position = (
        pupil_color_ramp_node.color_ramp.elements[0].position + 0.1
    )
    pupil_color_ramp_node.color_ramp.elements[1].color = (0, 0, 0, 1)

    mix_rgb_node = nodes.new("ShaderNodeMixRGB")
    mix_rgb_node.location = (-300, 200)
    mix_rgb_node.inputs["Color1"].default_value = color1
    mix_rgb_node.inputs["Color2"].default_value = color2

    invert_node = nodes.new("ShaderNodeInvert")
    invert_node.location = (-300, 400)

    displacement_node = nodes.new("ShaderNodeDisplacement")
    displacement_node.location = (-200, 0)
    displacement_node.inputs["Scale"].default_value = 0.05

    iris_mix_shader_node = nodes.new("ShaderNodeMixShader")
    iris_mix_shader_node.location = (0, 500)

    pupil_mix_shader_node = nodes.new("ShaderNodeMixShader")
    pupil_mix_shader_node.location = (0, 800)

    Principled_BSDF_node = nodes.get("Principled BSDF")
    Principled_BSDF_node.inputs["Metallic"].default_value = 0.5
    output_node = nodes.get("Material Output")

    links.new(texcoord_node.outputs["Object"], mapping_iris_node.inputs["Vector"])
    links.new(texcoord_node.outputs["Object"], mapping_pupil_node.inputs["Vector"])

    links.new(mapping_iris_node.outputs["Vector"], noise_node.inputs["Vector"])
    links.new(mapping_pupil_node.outputs["Vector"], gradient_node.inputs["Vector"])

    links.new(noise_node.outputs["Fac"], iris_color_ramp_node.inputs["Fac"])
    links.new(gradient_node.outputs["Fac"], pupil_color_ramp_node.inputs["Fac"])

    links.new(iris_color_ramp_node.outputs["Color"], mix_rgb_node.inputs["Fac"])
    links.new(
        pupil_color_ramp_node.outputs["Color"], pupil_mix_shader_node.inputs["Fac"]
    )

    links.new(mix_rgb_node.outputs["Color"], Principled_BSDF_node.inputs["Base Color"])
    links.new(mix_rgb_node.outputs["Color"], displacement_node.inputs["Height"])
    links.new(iris_color_ramp_node.outputs["Color"], invert_node.inputs["Color"])
    links.new(invert_node.outputs["Color"], iris_mix_shader_node.inputs["Fac"])

    links.new(Principled_BSDF_node.outputs["BSDF"], iris_mix_shader_node.inputs[1])
    links.new(iris_mix_shader_node.outputs["Shader"], pupil_mix_shader_node.inputs[2])

    links.new(pupil_mix_shader_node.outputs["Shader"], output_node.inputs["Surface"])

    links.new(
        displacement_node.outputs["Displacement"], output_node.inputs["Displacement"]
    )

    return mat


def add_eye_inside_material(pupil_size, color1, color2):
    ob = bpy.context.active_object

    # Get material

    mat = eye_inside_material(pupil_size, color1, color2)
    # Assign it to object
    if ob.data.materials:
        # assign to 1st material slot
        ob.data.materials[0] = mat
    else:
        # no slots
        ob.data.materials.append(mat)


class AddInside(bpy.types.Operator):
    """Add inside of eye"""

    bl_idname = "mesh.eye_inside"
    bl_label = "Add Eye Inside"
    bl_options = {"REGISTER", "UNDO"}

    pupil_size: FloatProperty(
        name="Pupil Size",
        description="Pupil Size",
        min=0.1,
        max=0.9,
        default=0.2,
    )

    color1: FloatVectorProperty(
        name="color1",
        subtype="COLOR",
        default=(0, 0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        size=4,
        description="color picker",
    )

    color2: FloatVectorProperty(
        name="color2",
        subtype="COLOR",
        default=(1.0, 0, 0, 1.0),
        min=0.0,
        max=1.0,
        size=4,
        description="color picker",
    )

    def execute(self, context):

        add_inside(self.pupil_size)
        add_eye_inside_material(self.pupil_size, self.color1, self.color2)

        return {"FINISHED"}


def register():
    bpy.utils.register_class(AddInside)


def unregister():
    bpy.utils.unregister_class(AddInside)


if __name__ == "__main__":
    register()
