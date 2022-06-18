import bpy

from .operators.add_inside import AddInside
from .operators.add_outside import AddOutside
from .operators.adjust import AdjustEye
from .operators.create import CreateEye
from .operators.mirror import MirrorEye
from .panels.aizen import AizenPanel

bl_info = {
    "name": "Aizen",
    "category": "Object",
    "author": "Xiangyi Gao",
    "blender": (3, 0, 0),
    "location": "View3D > right-side panel > Aizen",
    "description": "Addon to create an eye ball",
    "warning": "",
    "version": (0, 0, 1),
}

classes = [AddInside, AddOutside, CreateEye, AdjustEye, MirrorEye, AizenPanel]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
