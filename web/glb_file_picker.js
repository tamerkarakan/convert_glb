import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

function selectGlbFile() {
    return new Promise((resolve) => {
        const input = document.createElement("input");
        input.type = "file";
        input.accept = ".glb,.gltf,model/gltf-binary,model/gltf+json";
        input.style.display = "none";
        input.onchange = () => {
            resolve(input.files?.[0] ?? null);
            input.remove();
        };
        document.body.appendChild(input);
        input.click();
    });
}

async function uploadGlbFile(file) {
    const body = new FormData();
    body.append("file", file);

    const response = await api.fetchApi("/convert_glb/upload", {
        method: "POST",
        body,
    });

    const result = await response.json();
    if (!response.ok) {
        throw new Error(result?.error ?? "GLB upload failed.");
    }
    return result.path;
}

app.registerExtension({
    name: "convert_glb.file_picker",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "GLBFilePicker") {
            return;
        }

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            onNodeCreated?.apply(this, arguments);

            const pathWidget = this.widgets?.find((widget) => widget.name === "glb_path");
            if (!pathWidget) {
                return;
            }

            this.addWidget(
                "button",
                "Choose GLB/GLTF",
                null,
                async () => {
                    const file = await selectGlbFile();
                    if (!file) {
                        return;
                    }

                    try {
                        pathWidget.value = await uploadGlbFile(file);
                        this.graph?.setDirtyCanvas(true, true);
                    } catch (error) {
                        console.error("[convert_glb]", error);
                        alert(error.message ?? "GLB upload failed.");
                    }
                },
                { serialize: false }
            );
        };
    },
});
