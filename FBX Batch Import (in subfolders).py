bl_info = {
    "name": "Batch Import FBX in subfolder ",
    "author": "Muhammad",
    "description": "Batch generate default previews for the Asset Browser from selected folder",
    "blender": (3, 0, 0),
    "version": (0, 0, 2),
    "location": "",
    "warning": "",
    "category": "Import-Export",
}

from pathlib import Path
import bpy
import functools
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator



INTERVAL = 1.0


class ASSET_OT_batch_generate_previews(Operator, ImportHelper):
    bl_idname = "asset.batch_generate_previews"
    bl_label = "Batch Import FBX in subfolder"

    filter_glob: StringProperty(
        default="*.fbx",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    recursive: bpy.props.BoolProperty(
        default=True,
        name="Recursive",
        description="Operate on blend files located in sub folders recursively\nIf unchecked it will only treat files in this folder",
    )

    def execute(self, context):
        
        folder = Path(self.filepath)
        fbx_files = [f for f in folder.glob("**/*.fbx") if f.is_file()]
        for fbx_file in fbx_files:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.import_scene.fbx(filepath=str(fbx_file))
            for obj in bpy.context.selected_objects:
                obj.name = fbx_file.stem

        return {"FINISHED"}


def menu_func_import(self, context):
    self.layout.operator(ASSET_OT_batch_generate_previews.bl_idname, text=ASSET_OT_batch_generate_previews.bl_label)


def register():
    bpy.utils.register_class(ASSET_OT_batch_generate_previews)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.utils.unregister_class(ASSET_OT_batch_generate_previews)


if __name__ == "__main__":
    register()