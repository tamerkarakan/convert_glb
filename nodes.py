from __future__ import annotations

from pathlib import Path
from typing import Any

import trimesh


SUPPORTED_FORMATS = ("ply", "obj", "stl")


class GLBMeshConverter:
    """Convert a GLB/GLTF mesh to PLY, OBJ, or STL."""

    CATEGORY = "mesh/conversion"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_path",)
    FUNCTION = "convert"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "glb_path": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "Absolute or ComfyUI-relative path to a .glb or .gltf file.",
                    },
                ),
                "output_format": (SUPPORTED_FORMATS, {"default": "ply"}),
                "output_dir": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "Optional output folder. Empty means the input file folder.",
                    },
                ),
                "output_filename": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "Optional file name without extension. Empty means input file stem.",
                    },
                ),
                "overwrite": ("BOOLEAN", {"default": True}),
            }
        }

    def convert(
        self,
        glb_path: str,
        output_format: str,
        output_dir: str = "",
        output_filename: str = "",
        overwrite: bool = True,
    ) -> tuple[str]:
        input_path = self._resolve_input_path(glb_path)
        fmt = output_format.lower().strip()

        if fmt not in SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported output format '{output_format}'. Use one of: {', '.join(SUPPORTED_FORMATS)}")

        destination_dir = Path(output_dir).expanduser() if output_dir.strip() else input_path.parent
        destination_dir.mkdir(parents=True, exist_ok=True)

        safe_stem = output_filename.strip() or input_path.stem
        output_path = destination_dir / f"{Path(safe_stem).stem}.{fmt}"

        if output_path.exists() and not overwrite:
            raise FileExistsError(f"Output file already exists: {output_path}")

        mesh = self._load_as_mesh(input_path)
        mesh.export(output_path, file_type=fmt)

        return (str(output_path),)

    @staticmethod
    def _resolve_input_path(path_value: str) -> Path:
        cleaned = path_value.strip().strip('"')
        if not cleaned:
            raise ValueError("glb_path is required.")

        path = Path(cleaned).expanduser()
        if not path.is_absolute():
            path = Path.cwd() / path

        path = path.resolve()
        if not path.exists():
            raise FileNotFoundError(f"Input file was not found: {path}")
        if path.suffix.lower() not in {".glb", ".gltf"}:
            raise ValueError(f"Input must be a .glb or .gltf file: {path}")
        if not path.is_file():
            raise ValueError(f"Input path is not a file: {path}")

        return path

    @staticmethod
    def _load_as_mesh(path: Path) -> trimesh.Trimesh:
        loaded = trimesh.load(path, force="scene")

        if isinstance(loaded, trimesh.Trimesh):
            mesh = loaded
        elif isinstance(loaded, trimesh.Scene):
            dumped = loaded.dump(concatenate=True)
            if not isinstance(dumped, trimesh.Trimesh):
                raise ValueError(f"No mesh geometry found in: {path}")
            mesh = dumped
        else:
            raise ValueError(f"Could not load mesh from: {path}")

        if mesh.is_empty:
            raise ValueError(f"Loaded mesh is empty: {path}")

        return mesh
