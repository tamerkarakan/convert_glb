from .nodes import GLBMeshConverter

NODE_CLASS_MAPPINGS = {
    "GLBMeshConverter": GLBMeshConverter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GLBMeshConverter": "GLB Mesh Converter",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
