import bpy
from bpy.props import BoolProperty, FloatVectorProperty, IntProperty


def add_outside(size):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=64,
        ring_count=64,
        radius=1,
        enter_editmode=False,
        align="WORLD",
        location=(0, 0, 0),
        scale=(1, 1, 1),
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
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.ops.object.editmode_toggle()
    obj = bpy.context.active_object
    obj.data.vertices[1994].select = True
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_more()

    for _ in range(size):
        bpy.ops.mesh.select_more()

    bpy.ops.transform.translate(
        value=(-0, -0.05, -0),
        orient_type="GLOBAL",
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        orient_matrix_type="GLOBAL",
        constraint_axis=(False, True, False),
        mirror=True,
        use_proportional_edit=False,
        proportional_edit_falloff="SMOOTH",
        proportional_size=0.385543,
        use_proportional_connected=False,
        use_proportional_projected=False,
    )

    bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=10)
    bpy.ops.mesh.select_more()
    bpy.ops.mesh.region_to_loop()
    bpy.ops.view3d.snap_cursor_to_selected()

    bpy.ops.object.editmode_toggle()
    bpy.ops.object.shade_smooth()


def eye_outside_material(size, vein, color):
    bpy.context.scene.eevee.use_ssr = True
    bpy.context.scene.eevee.use_ssr_refraction = True

    mat = bpy.data.materials.new(name="Eye Outside")
    mat.use_nodes = True
    mat.use_screen_refraction = True
    mat.shadow_method = "NONE"

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    texcoord_node = nodes.new("ShaderNodeTexCoord")
    texcoord_node.location = (-1200, 100)

    mapping_glass_node = nodes.new("ShaderNodeMapping")
    mapping_glass_node.location = (-1000, 100)
    mapping_glass_node.inputs["Rotation"].default_value[1] = 1.5708

    glass_gradient_node = nodes.new("ShaderNodeTexGradient")
    glass_gradient_node.location = (-800, 100)

    glass_color_ramp_node = nodes.new("ShaderNodeValToRGB")
    glass_color_ramp_node.location = (-600, 100)

    glass_color_ramp_node.color_ramp.elements[0].position = (
        -0.0007 * (size**2) - 0.0121 * size + 0.9929
    ) + 0.02
    glass_color_ramp_node.color_ramp.elements[1].position = (
        glass_color_ramp_node.color_ramp.elements[0].position + 0.03
    )

    glass_mix_shader_node = nodes.new("ShaderNodeMixShader")
    glass_mix_shader_node.location = (300, 500)

    glass_shader_node = nodes.new("ShaderNodeBsdfGlass")
    glass_shader_node.location = (0, 500)
    glass_shader_node.inputs[2].default_value = 1.4

    if vein:
        mapping_vein_node = nodes.new("ShaderNodeMapping")
        mapping_vein_node.location = (-1000, -200)
        mapping_vein_node.inputs["Scale"].default_value[2] = 0
        vein_voronoi_node = nodes.new("ShaderNodeTexVoronoi")
        vein_voronoi_node.location = (-800, -200)
        vein_voronoi_node.feature = "DISTANCE_TO_EDGE"
        vein_voronoi_node.inputs["Scale"].default_value = 3.5

        vein_color_ramp_node = nodes.new("ShaderNodeValToRGB")
        vein_color_ramp_node.location = (-600, -200)
        vein_color_ramp_node.color_ramp.elements[1].position = 0.04

        vein_glass_color_ramp_node = nodes.new("ShaderNodeValToRGB")
        vein_glass_color_ramp_node.location = (-600, 400)

        vein_glass_color_ramp_node.color_ramp.elements[0].position = (
            glass_color_ramp_node.color_ramp.elements[0].position - 0.4
        )

        vein_math_node = nodes.new("ShaderNodeMath")
        vein_math_node.location = (-400, 0)
        vein_math_node.use_clamp = True

        vein_mix_rgb_node = nodes.new("ShaderNodeMixRGB")
        vein_mix_rgb_node.location = (-400, -200)
        vein_mix_rgb_node.inputs["Color1"].default_value = (0.5, 0, 0, 1)
        vein_mix_rgb_node.inputs["Color2"].default_value = color

        vein_noise_node = nodes.new("ShaderNodeTexNoise")
        vein_noise_node.location = (-1200, -200)
        vein_noise_node.inputs["Scale"].default_value = 0.5
        vein_noise_node.inputs["Detail"].default_value = 10
        vein_noise_node.inputs["Roughness"].default_value = 0.7

    Principled_BSDF_node = nodes.get("Principled BSDF")
    Principled_BSDF_node.inputs[0].default_value = color
    Principled_BSDF_node.inputs[1].default_value = 0.1
    Principled_BSDF_node.inputs[9].default_value = 0.1

    output_node = nodes.get("Material Output")

    if vein:
        links.new(
            glass_gradient_node.outputs["Color"],
            vein_glass_color_ramp_node.inputs["Fac"],
        )
        links.new(vein_glass_color_ramp_node.outputs["Color"], vein_math_node.inputs[0])
        links.new(texcoord_node.outputs["Object"], mapping_vein_node.inputs["Vector"])
        links.new(vein_noise_node.outputs["Fac"], mapping_vein_node.inputs["Location"])
        links.new(vein_noise_node.outputs["Fac"], mapping_vein_node.inputs["Rotation"])
        links.new(
            mapping_vein_node.outputs["Vector"], vein_voronoi_node.inputs["Vector"]
        )
        links.new(
            vein_voronoi_node.outputs["Distance"], vein_color_ramp_node.inputs["Fac"]
        )
        links.new(vein_color_ramp_node.outputs["Color"], vein_math_node.inputs[1])

        links.new(vein_math_node.outputs["Value"], vein_mix_rgb_node.inputs["Fac"])

        links.new(vein_mix_rgb_node.outputs["Color"], Principled_BSDF_node.inputs[0])
        links.new(vein_mix_rgb_node.outputs["Color"], Principled_BSDF_node.inputs[3])

    links.new(texcoord_node.outputs["Object"], mapping_glass_node.inputs["Vector"])
    links.new(
        mapping_glass_node.outputs["Vector"], glass_gradient_node.inputs["Vector"]
    )
    links.new(glass_gradient_node.outputs["Color"], glass_color_ramp_node.inputs["Fac"])

    links.new(
        glass_color_ramp_node.outputs["Color"], glass_mix_shader_node.inputs["Fac"]
    )

    links.new(Principled_BSDF_node.outputs["BSDF"], glass_mix_shader_node.inputs[1])
    links.new(glass_shader_node.outputs["BSDF"], glass_mix_shader_node.inputs[2])
    links.new(glass_mix_shader_node.outputs["Shader"], output_node.inputs["Surface"])

    return mat


def add_eye_outside_material(size, vein, color):
    ob = bpy.context.active_object

    # Get material

    mat = eye_outside_material(size, vein, color)
    # Assign it to object
    if ob.data.materials:
        # assign to 1st material slot
        ob.data.materials[0] = mat
    else:
        # no slots
        ob.data.materials.append(mat)


class AddOutside(bpy.types.Operator):
    """Add outside of eye"""

    bl_idname = "mesh.eye_outside"
    bl_label = "Add Eye Outside"
    bl_options = {"REGISTER", "UNDO"}

    glass_size: IntProperty(
        name="Glass Size",
        description="Glass Size",
        min=2,
        max=20,
        default=8,
    )
    vein: BoolProperty(name="vein", description="Enable or Disable Vein", default=True)
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

        add_outside(self.glass_size)
        add_eye_outside_material(self.glass_size, self.vein, self.eye_ball_color)

        return {"FINISHED"}


def register():
    bpy.utils.register_class(AddOutside)


def unregister():
    bpy.utils.unregister_class(AddOutside)


if __name__ == "__main__":
    register()
