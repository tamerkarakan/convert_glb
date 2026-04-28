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

The nodes appear as:

```text
mesh/conversion -> GLB File Picker
mesh/conversion -> GLB Mesh Converter
```

### GLB File Picker

Use `Choose GLB/GLTF` to select a local `.glb` or `.gltf` file in the browser. The file is uploaded into ComfyUI's `input/glb` folder and the node returns the server-side `glb_path`.

`glb_path` is also a connectable string input, so another node can provide the path directly.

### GLB Mesh Converter

Inputs:

- `glb_path`: connectable string input with the path to a `.glb` or `.gltf` file
- `output_format`: `ply`, `obj`, or `stl`
- `output_dir`: connectable optional output folder; empty writes to ComfyUI's output folder
- `output_filename`: connectable optional output file name without extension
- `overwrite`: whether to replace an existing output file

Output:

- `output_path`: converted mesh file path

Typical workflow:

```text
GLB File Picker.glb_path -> GLB Mesh Converter.glb_path
```
