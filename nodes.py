from __future__ import annotations

from pathlib import Path
import shutil
from time import time
from typing import Any

import trimesh

try:
    from aiohttp import web
    import folder_paths
    from server import PromptServer
except Exception:
    web = None
    folder_paths = None
    PromptServer = None


SUPPORTED_FORMATS = ("ply", "obj", "stl")
SUPPORTED_INPUT_FORMATS = {".glb", ".gltf"}


def _safe_upload_name(filename: str) -> str:
    stem = Path(filename).stem.replace(" ", "_")
    suffix = Path(filename).suffix.lower()
    safe_stem = "".join(char for char in stem if char.isalnum() or char in {"-", "_"}).strip("._")
    return f"{safe_stem or 'mesh'}{suffix}"


def _get_default_output_dir() -> Path:
    if folder_paths is not None:
        return Path(folder_paths.get_output_directory())
    return Path.cwd()


if PromptServer is not None and web is not None and folder_paths is not None:
    @PromptServer.instance.routes.post("/convert_glb/upload")
    async def upload_glb(request):
        data = await request.post()
        upload = data.get("file")

        if upload is None or not getattr(upload, "filename", ""):
            return web.json_response({"error": "No file was uploaded."}, status=400)

        suffix = Path(upload.filename).suffix.lower()
        if suffix not in SUPPORTED_INPUT_FORMATS:
            return web.json_response({"error": "Only .glb and .gltf files are supported."}, status=400)

        upload_dir = Path(folder_paths.get_input_directory()) / "glb"
        upload_dir.mkdir(parents=True, exist_ok=True)

        output_path = upload_dir / _safe_upload_name(upload.filename)
        if output_path.exists():
            output_path = output_path.with_stem(f"{output_path.stem}_{int(time())}")

        with output_path.open("wb") as output_file:
            shutil.copyfileobj(upload.file, output_file)

        return web.json_response({"path": str(output_path.resolve())})


class GLBFilePicker:
    """Upload/select a GLB/GLTF file and return its server-side path."""

    CATEGORY = "mesh/conversion"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("glb_path",)
    FUNCTION = "pick"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "glb_path": (
                    "STRING",
                    {
                        "default": "",
                        "forceInput": True,
                        "multiline": False,
                        "tooltip": "Use the Choose GLB/GLTF button to upload a file.",
                    },
                ),
            }
        }

    def pick(self, glb_path: str) -> tuple[str]:
        return (str(GLBMeshConverter._resolve_input_path(glb_path)),)


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
                        "forceInput": True,
                        "multiline": False,
                        "tooltip": "Absolute or ComfyUI-relative path to a .glb or .gltf file.",
                    },
                ),
                "output_format": (SUPPORTED_FORMATS, {"default": "ply"}),
                "output_dir": (
                    "STRING",
                    {
                        "default": "",
                        "forceInput": True,
                        "multiline": False,
                        "tooltip": "Optional output folder. Empty means ComfyUI's output folder.",
                    },
                ),
                "output_filename": (
                    "STRING",
                    {
                        "default": "",
                        "forceInput": True,
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

        destination_dir = Path(output_dir).expanduser() if output_dir.strip() else _get_default_output_dir()
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
        if path.suffix.lower() not in SUPPORTED_INPUT_FORMATS:
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
