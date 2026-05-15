from .nodes import COMFY_API_AVAILABLE, GLBFilePicker, GLBMeshConverter

if not COMFY_API_AVAILABLE:
    NODE_CLASS_MAPPINGS = {
        "GLBFilePicker": GLBFilePicker,
        "GLBMeshConverter": GLBMeshConverter,
    }

    NODE_DISPLAY_NAME_MAPPINGS = {
        "GLBFilePicker": "GLB File Picker",
        "GLBMeshConverter": "GLB Mesh Converter",
    }

WEB_DIRECTORY = "./web"

if COMFY_API_AVAILABLE:
    from .nodes import comfy_entrypoint

    __all__ = ["WEB_DIRECTORY", "comfy_entrypoint"]
else:
    __all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
