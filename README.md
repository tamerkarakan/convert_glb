# ComfyUI GLB Mesh Converter

ComfyUI custom node for converting `.glb` or `.gltf` files to `.ply`, `.obj`, or `.stl` using `trimesh`.

The node uses ComfyUI's modern V3 custom node API (`comfy_api.latest`) when available, with a V1 fallback for older ComfyUI installs.

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

The nodes appear as:

```text
mesh/conversion -> GLB File Picker
mesh/conversion -> GLB Mesh Converter
```

### GLB File Picker

Use `Choose GLB/GLTF` to select a local `.glb` or `.gltf` file in the browser. The file is uploaded into ComfyUI's `input/glb` folder and the node returns the server-side `glb_path`.

The selected path is written into the same `glb_path` field that you can also type or connect as a ComfyUI widget input.

### GLB Mesh Converter

Inputs:

- `glb_path`: `.glb` or `.gltf` file path
- `output_format`: `ply`, `obj`, or `stl`; defaults to `stl`
- `output_dir`: optional output folder; empty writes to ComfyUI's output folder
- `output_filename`: optional output file name without extension
- `overwrite`: whether to replace an existing output file

Output:

- `converted_model_path`: converted `.ply`, `.obj`, or `.stl` mesh file path

Typical workflow:

```text
GLB File Picker.glb_path -> GLB Mesh Converter.glb_path
```
