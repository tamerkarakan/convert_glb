# ComfyUI GLB Mesh Converter

ComfyUI custom node for converting `.glb` or `.gltf` files to `.ply`, `.obj`, or `.stl` using `trimesh`.

## Install

Place this folder under:

```text
ComfyUI/custom_nodes/convert_glb
```

Then install the dependency in the same Python environment ComfyUI uses:

```powershell
pip install -r ComfyUI/custom_nodes/convert_glb/requirements.txt
```

Restart ComfyUI.

## Node

The node appears as:

```text
mesh/conversion -> GLB Mesh Converter
```

Inputs:

- `glb_path`: path to a `.glb` or `.gltf` file
- `output_format`: `ply`, `obj`, or `stl`
- `output_dir`: optional output folder; empty writes next to the input file
- `output_filename`: optional output file name without extension
- `overwrite`: whether to replace an existing output file

Output:

- `output_path`: converted mesh file path
