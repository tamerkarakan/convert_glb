from .nodes import GLBFilePicker, GLBMeshConverter

NODE_CLASS_MAPPINGS = {
    "GLBFilePicker": GLBFilePicker,
    "GLBMeshConverter": GLBMeshConverter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GLBFilePicker": "GLB File Picker",
    "GLBMeshConverter": "GLB Mesh Converter",
}

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
